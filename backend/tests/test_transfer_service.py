"""Tests for TransferService - internal transfer logic."""

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType
from backend.services.transfer_service import AccountNotFoundError, InsufficientFundsError, TransferService


@pytest.fixture(name="session")
def session_fixture():
    """Creates an in-memory SQLite database for testing purposes."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_successful_transfer(session: Session):
    """Transfer creates an OUT record for sender and IN record for receiver."""
    sender = Account(user_id=1, account_number="PL00000000000000000000000001")
    receiver = Account(user_id=2, account_number="PL00000000000000000000000002")
    session.add(sender)
    session.add(receiver)
    session.add(Transaction(account_id=1, amount=1000.0, title="Initial funds", type=TransactionType.IN))
    session.commit()

    TransferService(session).execute_transfer(sender, "PL00000000000000000000000002", 200.0, "Test transfer")

    transfer_txns = session.exec(select(Transaction).where(Transaction.title == "Test transfer")).all()
    assert len(transfer_txns) == 2
    assert any(t.type == TransactionType.OUT and t.account_id == sender.id for t in transfer_txns)
    assert any(t.type == TransactionType.IN and t.account_id == receiver.id for t in transfer_txns)


def test_insufficient_funds(session: Session):
    """Transfer exceeding balance raises InsufficientFundsError and creates no records."""
    sender = Account(user_id=1, account_number="PL00000000000000000000000001")
    receiver = Account(user_id=2, account_number="PL00000000000000000000000002")
    session.add(sender)
    session.add(receiver)
    session.add(Transaction(account_id=1, amount=100.0, title="Initial funds", type=TransactionType.IN))
    session.commit()

    with pytest.raises(InsufficientFundsError):
        TransferService(session).execute_transfer(sender, "PL00000000000000000000000002", 500.0, "Too expensive")


def test_nonexistent_receiver(session: Session):
    """Transfer to unknown account number raises AccountNotFoundError."""
    sender = Account(user_id=1, account_number="PL00000000000000000000000001")
    session.add(sender)
    session.add(Transaction(account_id=1, amount=1000.0, title="Initial funds", type=TransactionType.IN))
    session.commit()

    with pytest.raises(AccountNotFoundError):
        TransferService(session).execute_transfer(sender, "PL99999999999999999999999999", 100.0, "Ghost transfer")