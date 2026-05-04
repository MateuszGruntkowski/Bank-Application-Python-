"""Notifications router - endpoints for notification management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def get_notifications(page: int = 1, per_page: int = 20, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all notifications for the current user."""
    # TODO: Implement using NotificationService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for NotificationService")



@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark a notification as read."""
    # TODO: Implement using NotificationService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for NotificationService")
