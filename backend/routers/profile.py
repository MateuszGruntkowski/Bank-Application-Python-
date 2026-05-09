"""Profile router - endpoints for user profile management."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.models.user_profile import UserProfile
from backend.services.user_profile_service import UserProfileService

router = APIRouter(prefix="/profile", tags=["Profile"])


class ProfileUpdateRequest(BaseModel):
    """Schema for updating user profile."""
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


@router.post("", response_model=UserProfile)
def create_profile(request: ProfileUpdateRequest, current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """Create current user's profile."""
    if not current_user.id:
        raise HTTPException(status_code=400, detail="Invalid user account")
    service = UserProfileService(db)

    if service.get_profile(current_user.id):
        raise HTTPException(status_code=400, detail="Profile already exists for this user")

    new_profile = UserProfile(
        user_id=current_user.id,
        first_name=request.first_name or "",
        last_name=request.last_name or "",
        phone=request.phone or ""
    )
    return service.create_profile(new_profile)


@router.get("", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's profile."""
    if not current_user.id:
        raise HTTPException(status_code=400, detail="Invalid user account")
    service = UserProfileService(db)
    profile = service.get_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("", response_model=UserProfile)
def update_profile(request: ProfileUpdateRequest, current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """Update current user's profile."""
    if not current_user.id:
        raise HTTPException(status_code=400, detail="Invalid user account")
    service = UserProfileService(db)
    update_data = request.model_dump(exclude_unset=True)
    profile = service.update_profile(current_user.id, update_data)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one first.")

    return profile
