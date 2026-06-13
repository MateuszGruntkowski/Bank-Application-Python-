"""
Loan model module.
Represents a loan application and its lifecycle in the banking system.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class LoanStatus(str, Enum):
    """Lifecycle states of a loan application."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REPAID = "REPAID"


class Loan(SQLModel, table=True):
    __tablename__ = "loans"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: float = Field(gt=0.0)
    remaining_amount: float = Field(gt=0.0)
    status: LoanStatus = Field(default=LoanStatus.PENDING)
    rejection_reason: Optional[str] = Field(default=None)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))