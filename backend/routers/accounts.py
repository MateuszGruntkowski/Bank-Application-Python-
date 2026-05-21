"""Accounts router - endpoints for account management."""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from datetime import datetime

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.models.account import Account
from backend.services.balance_calculator import BalanceCalculator
from backend.services.statement_generator import StatementGenerator
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
    date_from: datetime, date_to: datetime,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Generate and download a CSV bank statement."""
    # Looking for a bank account that belongs to the logged in user
    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()

    if not account:
        raise HTTPException(status_code=404, detail="Brak konta dla tego użytkownika")

    # Launch website
    generator = StatementGenerator(db)
    csv_content = generator.generate_csv(account.id, date_from, date_to)

    # Return the response as a file downloaded by the browser
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="bank_statement.csv"'}
    )


@router.get("/me/balance")
def get_my_balance(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Return the current balance for the logged-in user."""
    calculator = BalanceCalculator()
    balance = calculator.get_balance(current_user.id, db)
    return {"user_id": current_user.id, "balance": balance}