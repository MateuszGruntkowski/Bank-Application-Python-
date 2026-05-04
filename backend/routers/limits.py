"""Limits router - endpoints for transaction limit configuration."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/limits", tags=["Limits"])


class LimitsUpdateRequest(BaseModel):
    """Schema for updating transaction limits."""
    max_single_transfer: float | None = None
    max_daily_amount: float | None = None
    max_daily_count: int | None = None


@router.get("")
def get_limits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's transaction limits."""
    # TODO: Implement using TransactionLimitService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for TransactionLimitService")


@router.put("")
def update_limits(request: LimitsUpdateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user's transaction limits."""
    # TODO: Implement using TransactionLimitService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for TransactionLimitService")
