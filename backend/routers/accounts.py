"""Accounts router - endpoints for account management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.get("/me/transactions")
def get_my_transactions(
    page: int = 1, per_page: int = 10, sort_order: str = "desc",
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Return paginated transaction history for the current user."""
    # TODO: Implement using TransactionHistoryService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for TransactionHistoryService")


@router.get("/me/statement")
def get_statement(
    date_from: str = "", date_to: str = "",
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Generate and download a CSV bank statement."""
    # TODO: Implement using StatementGenerator
    raise HTTPException(status_code=501, detail="Not implemented - waiting for StatementGenerator")
