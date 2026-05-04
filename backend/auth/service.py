"""
Authentication service module.
Handles password hashing, JWT token creation and verification.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from sqlmodel import Session, select

from backend.models.user import User

SECRET_KEY = "bank-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


class AuthService:
    """Handles authentication: registration, login, token management."""

    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        """Hash a plain-text password using bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hashed password."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def create_access_token(self, user_id: int, username: str, is_admin: bool) -> str:
        """Create a JWT access token with user claims."""
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "username": username,
            "is_admin": is_admin,
            "exp": expire,
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> dict | None:
        """Decode and validate a JWT token. Returns claims or None."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None

    def register(self, username: str, email: str, password: str) -> User:
        """Register a new user. Raises ValueError on duplicate."""
        statement = select(User).where(
            (User.username == username) | (User.email == email)
        )
        existing = self.db.exec(statement).first()
        if existing:
            raise ValueError("Username or email already taken")

        user = User(
            username=username,
            email=email,
            hashed_password=self.hash_password(password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, username: str, password: str) -> dict:
        """Authenticate user and return token. Raises ValueError on failure."""
        statement = select(User).where(User.username == username)
        user = self.db.exec(statement).first()
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = self.create_access_token(user.id, user.username, user.is_admin)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        }

    def get_current_user(self, token: str) -> User:
        """Get user from JWT token. Raises ValueError if invalid."""
        payload = self.decode_token(token)
        if payload is None:
            raise ValueError("Invalid or expired token")

        user_id = int(payload.get("sub", 0))
        statement = select(User).where(User.id == user_id)
        user = self.db.exec(statement).first()
        if user is None:
            raise ValueError("User not found")
        return user
