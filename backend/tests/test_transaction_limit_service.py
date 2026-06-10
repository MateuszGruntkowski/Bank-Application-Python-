import pytest
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime, UTC

from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType
from backend.services.transaction_limit_service import TransactionLimitService

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_update_limits_successfully(session: Session):
    account = Account(user_id=1, account_number="TEST_LIMITS_1", single_transfer_limit=100.0, daily_limit=500.0)
    session.add(account)
    session.commit()

    service = TransactionLimitService(session)
    service.update_limits(account.id, new_daily_limit=2000.0, new_single_limit=1000.0)

    session.refresh(account)
    assert account.daily_limit == 2000.0
    assert account.single_transfer_limit == 1000.0


def test_single_transfer_limit_exceeded(session: Session):
    account = Account(user_id=2, account_number="TEST_LIMITS_2", single_transfer_limit=50.0, daily_limit=500.0)
    session.add(account)
    session.commit()

    service = TransactionLimitService(session)

    with pytest.raises(HTTPException) as exc_info:
        service.validate_transfer_limits(account, amount=100.0)

    assert exc_info.value.status_code == 400
    assert "exceeds single transfer limit" in exc_info.value.detail


def test_daily_transfer_limit_exceeded(session: Session):
    account = Account(user_id=3, account_number="TEST_LIMITS_3", single_transfer_limit=500.0, daily_limit=200.0)
    session.add(account)
    session.commit()

    tx = Transaction(
        account_id=account.id,
        amount=150.0,
        type=TransactionType.OUT,
        title="Last transfer",
        created_at=datetime.now(UTC)
    )
    session.add(tx)
    session.commit()

    service = TransactionLimitService(session)

    with pytest.raises(HTTPException) as exc_info:
        service.validate_transfer_limits(account, amount=100.0)

    assert exc_info.value.status_code == 400
    assert "Exceeded daily limit" in exc_info.value.detail