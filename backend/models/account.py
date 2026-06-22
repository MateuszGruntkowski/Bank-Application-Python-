"""Account model for the banking system."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    """Represents a bank account linked to a user."""

    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    account_number: str = Field(max_length=28, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    daily_limit: float = Field(default=5000.0)
    single_transfer_limit: float = Field(default=2000.0)
    daily_count_limit: int = Field(default=10)