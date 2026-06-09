"""Transfers router - endpoints for internal and external transfers."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.account import Account
from backend.models.user import User
from backend.services.transfer_service import AccountNotFoundError, InsufficientFundsError, TransferService
from backend.services.external_transfer_service import ExternalTransferService

router = APIRouter(prefix="/transfers", tags=["Transfers"])


class TransferRequest(BaseModel):
    """Schema for a transfer."""
    to_account_number: str
    amount: float
    title: str


@router.post("")
def make_transfer(request: TransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Execute an internal transfer between accounts."""
    # Get sender's account
    statement = select(Account).where(Account.user_id == current_user.id)
    from_account = db.exec(statement).first()
    if from_account is None:
        raise HTTPException(status_code=404, detail="Sender account not found.")

    service = TransferService(session=db)

    try:
        service.execute_transfer(
            from_account=from_account,
            to_account_number=request.to_account_number,
            amount=request.amount,
            title=request.title,
        )
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Transfer completed successfully."}


@router.post("/external")
def make_external_transfer(request: TransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Execute a transfer to an external account."""
    statement = select(Account).where(Account.user_id == current_user.id)
    from_account = db.exec(statement).first()
    if from_account is None:
        raise HTTPException(status_code=404, detail="Sender account not found.")

    service = ExternalTransferService(session=db)

    try:
        service.execute_transfer(
            from_account=from_account,
            to_account_number=request.to_account_number,
            amount=request.amount,
            title=request.title,
        )
    except InsufficientFundsError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"message": "Transfer completed successfully."}
