"""
Database seeder - creates initial admin user and test data.
Run once on first startup to populate the database.
"""

from sqlmodel import Session, select

from backend.auth.service import AuthService
from backend.database import engine
from backend.models.account import Account
from backend.models.user import User


def _generate_account_number(index: int) -> str:
    """Generate a deterministic account number for seeding."""
    base = str(index).zfill(26)
    return f"PL{base}"


def seed():
    """Populate the database with initial data if empty."""
    with Session(engine) as db:
        existing = db.exec(select(User)).first()
        if existing:
            return

        auth = AuthService(db)

        # Create admin user
        admin = User(
            username="admin",
            email="admin@bank.io",
            hashed_password=auth.hash_password("admin"),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        db.add(Account(user_id=admin.id, account_number=_generate_account_number(1)))

        # Create test users
        for i, (name, email) in enumerate([
            ("jan_kowalski", "jan@bank.io"),
            ("anna_nowak", "anna@bank.io"),
        ], start=2):
            user = User(
                username=name,
                email=email,
                hashed_password=auth.hash_password("password123"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db.add(Account(user_id=user.id, account_number=_generate_account_number(i)))

        db.commit()


if __name__ == "__main__":
    from backend.database import init_db
    init_db()
    seed()
    print("Database seeded successfully.")
