"""Standing orders router - endpoints for recurring payment management."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/standing-orders", tags=["Standing Orders"])


class CreateOrderRequest(BaseModel):
    """Schema for creating a standing order."""
    to_account_number: str
    amount: float
    title: str
    frequency: str  # WEEKLY or MONTHLY


@router.get("")
def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all standing orders for the current user."""
    # TODO: Implement using StandingOrderService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for StandingOrderService")


@router.post("")
def create_order(request: CreateOrderRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new standing order."""
    # TODO: Implement using StandingOrderService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for StandingOrderService")


@router.delete("/{order_id}")
def cancel_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cancel a standing order."""
    # TODO: Implement using StandingOrderService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for StandingOrderService")
