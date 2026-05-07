"""Accounts router - endpoints for account management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.services.balance_calculator import BalanceCalculator

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


@router.get("/me/balance")
def get_my_balance(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Return the current balance for the logged-in user."""
    calculator = BalanceCalculator()
    balance = calculator.get_balance(current_user.id, db)
    return {"user_id": current_user.id, "balance": balance}