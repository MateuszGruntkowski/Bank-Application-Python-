"""
Unit tests for LoanApplicationService.

Uses an in-memory SQLite database (via SQLModel) so no real DB is needed.
Each test gets a fresh, isolated session.
"""

import pytest
from sqlmodel import Session, SQLModel, create_engine

from backend.models.loan import Loan, LoanStatus
from backend.models.user import User
from backend.services.loan_application_service import (
    ACTIVE_LOAN_STATUSES,
    LoanApplicationError,
    LoanApplicationService,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(name="engine")
def engine_fixture():
    """In-memory SQLite engine with all tables created fresh for every test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="db")
def db_fixture(engine):
    """Provide a clean Session per test."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="user")
def user_fixture(db: Session) -> User:
    """Persist and return a basic test user."""
    u = User(
        username="jan_kowalski",
        email="jan@example.com",
        hashed_password="hashed_secret",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _add_loan(db: Session, user: User, status: LoanStatus, amount: float = 1000.0) -> Loan:
    """Helper – insert a loan in a given status directly (bypassing the service)."""
    loan = Loan(
        user_id=user.id,
        amount=amount,
        remaining_amount=amount,
        status=status,
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

class TestApplyHappyPath:

    def test_returns_loan_with_pending_status(self, db: Session, user: User):
        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=5000.0)

        assert loan.id is not None
        assert loan.status == LoanStatus.PENDING

    def test_loan_has_correct_amount(self, db: Session, user: User):
        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=2500.0)

        assert loan.amount == 2500.0
        assert loan.remaining_amount == 2500.0

    def test_loan_is_linked_to_user(self, db: Session, user: User):
        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=1000.0)

        assert loan.user_id == user.id

    def test_apply_allowed_after_rejected_loan(self, db: Session, user: User):
        """A REJECTED loan must not block a new application."""
        _add_loan(db, user, LoanStatus.REJECTED)

        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=3000.0)

        assert loan.status == LoanStatus.PENDING

    def test_apply_allowed_after_repaid_loan(self, db: Session, user: User):
        """A fully REPAID loan must not block a new application."""
        _add_loan(db, user, LoanStatus.REPAID)

        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=3000.0)

        assert loan.status == LoanStatus.PENDING


class TestActiveLoanGuard:

    @pytest.mark.parametrize("blocking_status", list(ACTIVE_LOAN_STATUSES))
    def test_raises_when_active_loan_exists(
        self, db: Session, user: User, blocking_status: LoanStatus
    ):
        """Each active status (PENDING, APPROVED) must block a second application."""
        _add_loan(db, user, blocking_status)

        service = LoanApplicationService(db)
        with pytest.raises(LoanApplicationError, match="active loan"):
            service.apply(user=user, amount=500.0)

    def test_guard_is_per_user(self, db: Session, user: User, engine):
        """Active loan of user A must not block user B."""
        _add_loan(db, user, LoanStatus.PENDING)

        other = User(
            username="anna_nowak",
            email="anna@example.com",
            hashed_password="hashed",
        )
        db.add(other)
        db.commit()
        db.refresh(other)

        service = LoanApplicationService(db)
        loan = service.apply(user=other, amount=1000.0)
        assert loan.status == LoanStatus.PENDING

class TestAmountValidation:

    def test_zero_amount_raises(self, db: Session, user: User):
        service = LoanApplicationService(db)
        with pytest.raises(LoanApplicationError, match="greater than zero"):
            service.apply(user=user, amount=0.0)

    def test_negative_amount_raises(self, db: Session, user: User):
        service = LoanApplicationService(db)
        with pytest.raises(LoanApplicationError, match="greater than zero"):
            service.apply(user=user, amount=-100.0)

    def test_very_small_positive_amount_is_accepted(self, db: Session, user: User):
        service = LoanApplicationService(db)
        loan = service.apply(user=user, amount=0.01)
        assert loan.amount == pytest.approx(0.01)