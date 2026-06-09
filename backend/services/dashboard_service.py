from sqlmodel import Session, select

from backend.models.transaction import Transaction
from backend.services.balance_calculator import BalanceCalculator

class DashboardService:
    """Service responsible for dashboard aggregation."""

    def __init__(self, session: Session):
        self.session = session

    def get_dashboard(self, user_id: int) -> dict:
        """Returns aggregated dashboard data for user."""

        return {
            "account": {"user_id": user_id},
            "balance": BalanceCalculator().get_balance(user_id, self.session),
            "last_transactions": self.session.exec(
                select(Transaction)
                .where(Transaction.account_id == user_id)
                .order_by(Transaction.created_at.desc())
                .limit(5)
            ).all(),
            "unread_notifications": 0,
        }
