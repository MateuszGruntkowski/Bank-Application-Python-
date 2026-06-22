"""
Authentication router.
Handles /auth/register, /auth/login and /auth/me endpoints.
"""

import random
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session

from backend.auth.service import AuthService
from backend.database import get_db
from backend.models.account import Account
from backend.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    """Schema for user registration."""

    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Schema for user login."""

    username: str
    password: str

def _get_token(authorization: Optional[str] = Header(None)) -> str:
    """Extract Bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid authorization header"
        )
    return authorization.replace("Bearer ", "")


def get_current_user(
    token: str = Depends(_get_token),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency to get current authenticated user."""
    auth_service = AuthService(db)
    try:
        return auth_service.get_current_user(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """FastAPI dependency that requires admin privileges."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


def _generate_account_number() -> str:
    """Generate a random Polish-format bank account number."""
    digits = "".join([str(random.randint(0, 9)) for _ in range(26)])
    return f"PL{digits}"


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and create their bank account."""
    auth_service = AuthService(db)
    try:
        user = auth_service.register(request.username, request.email, request.password)
        account = Account(
            user_id=user.id,
            account_number=_generate_account_number(),
        )
        db.add(account)
        db.commit()
        return {"message": "Registration successful", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    auth_service = AuthService(db)
    try:
        return auth_service.login(request.username, request.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Return current user's basic info."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
    }
