"""Dashboard router - aggregated dashboard data endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return aggregated dashboard data for the current user."""
    # TODO: Implement using DashboardService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for DashboardService")
