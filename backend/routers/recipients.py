"""Recipients router - endpoints for managing saved transfer recipients."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

from backend.services.recipient_service import RecipientService

router = APIRouter(prefix="/recipients", tags=["Recipients"])


class RecipientRequest(BaseModel):
    """Schema for adding a recipient."""
    name: str
    account_number: str


@router.get("")
def get_recipients(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of saved recipients for the current user."""
    service = RecipientService(db)
    return service.get_recipients(user_id=current_user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
def add_recipient(request: RecipientRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Add a new saved recipient."""
    service = RecipientService(db)
    return service.add_recipient(
        user_id=current_user.id,
        name=request.name,
        account_number=request.account_number
    )


@router.delete("/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recipient(recipient_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Remove a saved recipient."""
    service = RecipientService(db)

    success = service.delete_recipient(user_id=current_user.id, recipient_id=recipient_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found or you don't have permission to delete it"
        )
    return None