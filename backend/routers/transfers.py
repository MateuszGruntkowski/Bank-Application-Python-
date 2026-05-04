"""Transfers router - endpoints for internal and external transfers."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/transfers", tags=["Transfers"])


class TransferRequest(BaseModel):
    """Schema for a transfer."""
    to_account_number: str
    amount: float
    title: str


@router.post("")
def make_transfer(request: TransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Execute an internal transfer between accounts."""
    # TODO: Implement using TransferService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for TransferService")


@router.post("/external")
def make_external_transfer(request: TransferRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Execute a transfer to an external account."""
    # TODO: Implement using ExternalTransferService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for ExternalTransferService")
