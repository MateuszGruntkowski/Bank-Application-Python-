"""Accounts router - endpoints for account management."""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from datetime import datetime
import math

from backend.auth import get_current_user
from backend.database import get_db
from backend.models.user import User
from backend.models.account import Account
from backend.services.balance_calculator import BalanceCalculator
from backend.services.statement_generator import StatementGenerator
from backend.services.transaction_history_service import TransactionHistoryService

router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.get("/me/transactions")
def get_my_transactions(
        page: int = 1,
        per_page: int = 10,
        sort_order: str = "desc",
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Return paginated transaction history for the current user."""

    account = db.exec(select(Account).where(Account.user_id == current_user.id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    limit = per_page
    offset = (page - 1) * per_page

    service = TransactionHistoryService(db)
    transactions = service.get_history(account_id=account.id, limit=limit, offset=offset, sort_order=sort_order)

    total_transactions = service.get_total_count(account_id=account.id)
    total_pages = math.ceil(total_transactions / per_page)

    formatted_transactions = []
    for tx in transactions:
        tx_data = tx.model_dump() if hasattr(tx, "model_dump") else tx.model_dump()
        if tx.created_at:
            tx_data["created_at"] = tx.created_at.strftime("%d.%m.%Y %H:%M")

        formatted_transactions.append(tx_data)

    return {
        "transactions": formatted_transactions,
        "total": total_transactions,
        "pages": total_pages
    }
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