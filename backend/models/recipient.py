"""Model representing a saved transfer recipient."""

from typing import Optional
from sqlmodel import SQLModel, Field

class Recipient(SQLModel, table=True):
    """Database model for saved recipients."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    account_number: str  