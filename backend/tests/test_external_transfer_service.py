"""Tests for ExternalTransferService."""

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType
from backend.services.external_transfer_service import ExternalTransferService
from backend.services.transfer_service import InsufficientFundsError


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="sender")
def sender_fixture(session: Session):
    account = Account(user_id=1, account_number="PL00000000000000000000000001")
    session.add(account)
    session.add(Transaction(account_id=1, amount=1000.0, title="Initial funds", type=TransactionType.IN))
    session.commit()
    session.refresh(account)
    return account


def test_external_transfer_creates_single_out_external_record(session: Session, sender: Account):
    """Successful external transfer creates exactly one OUT_EXTERNAL record."""
    ExternalTransferService(session).execute_transfer(
        sender, "DE89370400440532013000", 200.0, "External payment"
    )

    txns = session.exec(select(Transaction).where(Transaction.title == "External payment")).all()
    assert len(txns) == 1
    assert txns[0].type == TransactionType.OUT_EXTERNAL
    assert txns[0].account_id == sender.id


def test_external_transfer_no_incoming_record(session: Session, sender: Account):
    """External transfer must NOT create an IN record anywhere."""
    ExternalTransferService(session).execute_transfer(
        sender, "DE89370400440532013000", 200.0, "External payment"
    )

    in_txns = session.exec(
        select(Transaction).where(
            Transaction.type == TransactionType.IN,
            Transaction.title == "External payment"
        )
    ).all()
    assert len(in_txns) == 0


def test_external_transfer_insufficient_funds(session: Session, sender: Account):
    """Transfer exceeding balance raises InsufficientFundsError and creates no records."""
    with pytest.raises(InsufficientFundsError):
        ExternalTransferService(session).execute_transfer(
            sender, "DE89370400440532013000", 9999.0, "Too expensive"
        )

    txns = session.exec(select(Transaction).where(Transaction.title == "Too expensive")).all()
    assert len(txns) == 0


def test_external_transfer_does_not_verify_recipient(session: Session, sender: Account):
    """External transfer succeeds even when recipient account doesn't exist in the system."""
    ExternalTransferService(session).execute_transfer(
        sender, "UNKNOWN_EXTERNAL_ACCOUNT", 50.0, "To unknown"
    )

    txns = session.exec(select(Transaction).where(Transaction.title == "To unknown")).all()
    assert len(txns) == 1
    assert txns[0].type == TransactionType.OUT_EXTERNAL