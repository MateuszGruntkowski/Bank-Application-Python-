"""User Profile model for the banking system."""

from typing import Optional
from sqlmodel import Field, SQLModel


class UserProfile(SQLModel, table=True):
    """Represents a user's contact profile in the banking system."""

    __tablename__ = "user_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    # This entry Foreign_key="users.id" links your profile to the 'users' table
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    first_name: str
    last_name: str
    phone: str
