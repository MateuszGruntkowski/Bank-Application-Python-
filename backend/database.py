"""
Database configuration module.
Sets up SQLModel engine and session for SQLite.
"""

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./bank.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_db():
    """FastAPI dependency that provides a database session."""
    with Session(engine) as session:
        yield session

from backend.models.user import User
from backend.models.account import Account
from backend.models.transaction import Transaction

def init_db():
    """Create all tables defined by SQLModel subclasses."""
    SQLModel.metadata.create_all(engine)
