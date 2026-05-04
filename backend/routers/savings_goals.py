"""Savings goals router - endpoints for savings goal management."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/savings-goals", tags=["Savings Goals"])


class CreateGoalRequest(BaseModel):
    """Schema for creating a savings goal."""
    name: str
    target_amount: float
    deadline: str


class GoalFundsRequest(BaseModel):
    """Schema for adding/withdrawing funds from a goal."""
    amount: float


@router.get("")
def get_goals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all savings goals for the current user."""
    # TODO: Implement using SavingsGoalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for SavingsGoalService")


@router.post("")
def create_goal(request: CreateGoalRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new savings goal."""
    # TODO: Implement using SavingsGoalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for SavingsGoalService")


@router.post("/{goal_id}/deposit")
def deposit_to_goal(goal_id: int, request: GoalFundsRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Add funds to a savings goal from the main account."""
    # TODO: Implement using SavingsGoalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for SavingsGoalService")


@router.post("/{goal_id}/withdraw")
def withdraw_from_goal(goal_id: int, request: GoalFundsRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Withdraw funds from a savings goal to the main account."""
    # TODO: Implement using SavingsGoalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for SavingsGoalService")
