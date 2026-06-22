"""
Loan application service module.
Handles the business logic for submitting a loan application,
including validation that the user has no existing active loan.
"""

from datetime import datetime, timezone

from sqlmodel import Session, select

from backend.models.loan import Loan, LoanStatus
from backend.models.user import User


# Statuses that count as "active" – user must not have any of these to apply.
ACTIVE_LOAN_STATUSES = {LoanStatus.PENDING, LoanStatus.APPROVED}


class LoanApplicationError(Exception):
    """Raised when a loan application cannot be submitted."""


class LoanApplicationService:
    """Handles loan application submission with business-rule validation."""

    def __init__(self, db: Session):
        self.db = db

    def apply(self, user: User, amount: float) -> Loan:
        """
        Submit a new loan application for *user*.

        Raises:
            LoanApplicationError: if the user already has an active loan
                                   or if the requested amount is invalid.
        """
        self._validate_amount(amount)
        self._validate_no_active_loan(user)

        loan = Loan(
            user_id=user.id,
            amount=amount,
            remaining_amount=amount,
            status=LoanStatus.PENDING,
        )
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def _validate_amount(self, amount: float) -> None:
        """Ensure the requested amount is a positive number."""
        if amount <= 0:
            raise LoanApplicationError("Loan amount must be greater than zero.")

    def _validate_no_active_loan(self, user: User) -> None:
        """
        Ensure the user has no loan with an active status.

        An active loan is one with status PENDING or APPROVED.
        A REPAID or REJECTED loan does not block a new application.
        """
        statement = (
            select(Loan)
            .where(Loan.user_id == user.id)
            .where(Loan.status.in_(ACTIVE_LOAN_STATUSES))  # type: ignore[attr-defined]
        )
        existing = self.db.exec(statement).first()
        if existing is not None:
            raise LoanApplicationError(
                f"User already has an active loan"
            )