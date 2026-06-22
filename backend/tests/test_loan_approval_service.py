import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from fastapi import HTTPException

from backend.models.loan import Loan, LoanStatus
from backend.models.account import Account
from backend.models.user import User
from backend.models.transaction import Transaction
from backend.services.loan_approval_service import LoanApprovalService


# Preparing a fake database in RAM (Fixture)
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# test data (Customer, Account, Application)
@pytest.fixture
def setup_data(session: Session):
    # create a user
    user = User(username="janek", email="janek@test.pl", hashed_password="secret")
    session.add(user)
    session.commit()

    # creating an account for him
    account = Account(user_id=user.id, account_number="1234567890", balance=0.0)
    session.add(account)
    session.commit()

    # creating a pending application (PENDING)
    loan = Loan(user_id=user.id, amount=5000.0, remaining_amount=5000.0, status=LoanStatus.PENDING)
    session.add(loan)
    session.commit()

    return {"user": user, "account": account, "loan": loan}


# TESTS

def test_approve_loan_success(session: Session, setup_data):
    """The test checks whether the status changes after acceptance and a transfer is created."""
    service = LoanApprovalService(session)
    loan_id = setup_data["loan"].id
    account_id = setup_data["account"].id

    approved_loan = service.approve_loan(loan_id)

    # checking the status
    assert approved_loan.status == LoanStatus.APPROVED

    # check whether a transfer of 5000 has been generated
    transaction = session.exec(select(Transaction).where(Transaction.account_id == account_id)).first()
    assert transaction is not None
    assert transaction.amount == 5000.0
    assert transaction.type == "IN"


def test_reject_loan_success(session: Session, setup_data):
    """The test checks whether the application is correctly rejected with a reason given."""
    service = LoanApprovalService(session)
    loan_id = setup_data["loan"].id
    reason = "Zbyt niskie dochody"

    rejected_loan = service.reject_loan(loan_id, reason)

    # check the status and reason for rejection
    assert rejected_loan.status == LoanStatus.REJECTED
    assert rejected_loan.rejection_reason == reason


def test_approve_loan_already_processed(session: Session, setup_data):
    """The test checks the security against reconsideration of the application."""
    service = LoanApprovalService(session)
    loan_id = setup_data["loan"].id

    # deliberately rejecting the application
    service.reject_loan(loan_id, "Test odrzucenia")

    # trying to accept an already rejected request (should throw an error)
    with pytest.raises(HTTPException) as excinfo:
        service.approve_loan(loan_id)

    # make sure that the error thrown is 400 Bad Request
    assert excinfo.value.status_code == 400
