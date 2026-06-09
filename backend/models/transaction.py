from typing import Optional
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel

class TransactionType(str, Enum):
    """Enumeration for transaction types (income / outcome)."""
    IN = "IN"
    OUT = "OUT"
    OUT_EXTERNAL = "OUT_EXTERNAL"

class Transaction(SQLModel, table=True):
    """
    Database model representing a single transaction record.
    A single transfer between users creates two records (sender's OUT, receiver's IN).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(index=True)
    amount: float = Field(gt=0.0)
    title: str
    type: TransactionType
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))