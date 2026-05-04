"""ATM router - endpoints for cash deposit and withdrawal."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/atm", tags=["ATM"])


class ATMRequest(BaseModel):
    """Schema for ATM deposit/withdrawal."""
    amount: float


@router.post("/deposit")
def deposit(request: ATMRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Deposit cash into the current user's account."""
    # TODO: Implement using ATMService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for ATMService")


@router.post("/withdraw")
def withdraw(request: ATMRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Withdraw cash from the current user's account."""
    # TODO: Implement using ATMService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for ATMService")
