"""Profile router - endpoints for user profile management."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])


class ProfileUpdateRequest(BaseModel):
    """Schema for updating user profile."""
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


@router.get("")
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's profile."""
    # TODO: Implement using UserProfileService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for UserProfileService")


@router.put("")
def update_profile(request: ProfileUpdateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user's profile."""
    # TODO: Implement using UserProfileService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for UserProfileService")
