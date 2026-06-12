from datetime import datetime, time, UTC
from sqlmodel import Session, select
from fastapi import HTTPException, status

from backend.models.account import Account
from backend.models.transaction import Transaction


class TransactionLimitService:
    def __init__(self, session: Session):
        self.session = session

    def validate_transfer_limits(self, account: Account, amount: float):
        """Checks if transfer amount fits in accounts transfer limits."""

        if amount > account.single_transfer_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transfer denied: Transfer amount: ({amount}) exceeds single transfer limit: ({account.single_transfer_limit})."
            )


        today_start = datetime.combine(datetime.now(UTC).date(), time.min, tzinfo=UTC)

        statement = select(Transaction).where(
            Transaction.account_id == account.id,
            Transaction.type == "OUT",
            Transaction.created_at >= today_start
        )
        today_transactions = self.session.exec(statement).all()

        if len(today_transactions) >= account.daily_count_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transfer denied: Exceeded daily count limit. "
                       f"You already made {len(today_transactions)} transfers today. Your limit is: {account.daily_count_limit}."
            )

        current_daily_total = sum(t.amount for t in today_transactions)

        if current_daily_total + amount > account.daily_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transfer denied: Exceeded daily limit. "
                       f"Today already transferred: {current_daily_total}, Your limit is: {account.daily_limit}."
            )

    def update_limits(self, account_id: int, new_daily_limit: float, new_single_limit: float, new_daily_count: int) -> Account:
        """Updates database with new transfer limits set by client."""
        statement = select(Account).where(Account.id == account_id)
        account = self.session.exec(statement).first()

        if not account:
            raise HTTPException(status_code=404, detail="Couldn't find an account with that id.")

        account.daily_limit = new_daily_limit
        account.single_transfer_limit = new_single_limit
        account.daily_count_limit = new_daily_count

        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)

        return account