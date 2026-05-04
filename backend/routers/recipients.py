"""Recipients router - endpoints for managing saved transfer recipients."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/recipients", tags=["Recipients"])


class RecipientRequest(BaseModel):
    """Schema for adding a recipient."""
    name: str
    account_number: str


@router.get("")
def get_recipients(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of saved recipients for the current user."""
    # TODO: Implement using RecipientService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for RecipientService")


@router.post("")
def add_recipient(request: RecipientRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Add a new saved recipient."""
    # TODO: Implement using RecipientService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for RecipientService")


@router.delete("/{recipient_id}")
def remove_recipient(recipient_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Remove a saved recipient."""
    # TODO: Implement using RecipientService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for RecipientService")
