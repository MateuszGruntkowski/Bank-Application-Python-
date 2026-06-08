"""ATM router - endpoints for cash deposit and withdrawal."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.models.account import Account
from backend.services.atm_service import ATMService

router = APIRouter(prefix="/atm", tags=["ATM"])


class ATMRequest(BaseModel):
    """Schema for ATM deposit/withdrawal."""
    amount: float


@router.post("/deposit")
def deposit(request: ATMRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Deposit cash into the current user's account."""
    # TODO: Implement using ATMService
    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()
    if not account:
        raise HTTPException(404, "Account not found")

    ATMService(db).deposit(account.id, request.amount)
    return {"message": "Deposit successful"}

@router.post("/withdraw")
def withdraw(request: ATMRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Withdraw cash from the current user's account."""
    # TODO: Implement using ATMService
    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()
    if not account:
        raise HTTPException(404, "Account not found")

    try:
        ATMService(db).withdraw(account.id, request.amount)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"message": "Withdrawal successful"}
