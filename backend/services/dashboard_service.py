from sqlmodel import Session, select, func

from backend.models import Loan
from backend.models.loan import LoanStatus
from backend.models.transaction import Transaction
from backend.services.balance_calculator import BalanceCalculator
from backend.services.loan_application_service import ACTIVE_LOAN_STATUSES


class DashboardService:
    """Service responsible for dashboard aggregation."""

    def __init__(self, session: Session):
        self.session = session

    def get_dashboard(self, user_id: int) -> dict:
        """Returns aggregated dashboard data for user."""

        return {
            "account": {"user_id": user_id},
            "balance": BalanceCalculator().get_balance(user_id, self.session),
            "recent_transactions": self.session.exec(
                select(Transaction)
                .where(Transaction.account_id == user_id)
                .order_by(Transaction.created_at.desc())
                .limit(5)
            ).all(),
            "transaction_count": self.session.exec(
                select(func.count(Transaction.id))
                .where(Transaction.account_id == user_id)
            ).one(),
            "active_loans": self.session.exec(
                select(func.count(Loan.id))
                .where(Loan.user_id == user_id, Loan.status.in_(ACTIVE_LOAN_STATUSES))
            ).one(),
            "unread_notifications": 0,
        }
