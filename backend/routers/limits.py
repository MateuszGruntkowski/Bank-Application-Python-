"""Limits router - endpoints for transaction limit configuration."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.models.account import Account
from backend.services.transaction_limit_service import TransactionLimitService


router = APIRouter(prefix="/limits", tags=["Limits"])


class LimitsUpdateRequest(BaseModel):
    """Schema for updating transaction limits."""
    max_single_transfer: float | None = None
    max_daily_amount: float | None = None
    max_daily_count: int | None = None


@router.get("")
def get_limits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's transaction limits."""
    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    return {
        "max_single_transfer": account.single_transfer_limit,
        "max_daily_amount": account.daily_limit,
        "max_daily_count": None
    }


@router.put("")
def update_limits(request: LimitsUpdateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user's transaction limits."""
    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    new_daily = request.max_daily_amount if request.max_daily_amount is not None else account.daily_limit
    new_single = request.max_single_transfer if request.max_single_transfer is not None else account.single_transfer_limit

    limit_service = TransactionLimitService(db)
    updated_account = limit_service.update_limits(
        account_id=account.id,
        new_daily_limit=new_daily,
        new_single_limit=new_single
    )

    return {
        "max_single_transfer": updated_account.single_transfer_limit,
        "max_daily_amount": updated_account.daily_limit,
        "max_daily_count": None
    }
