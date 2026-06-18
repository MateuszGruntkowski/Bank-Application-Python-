import pytest
from sqlmodel import Session, SQLModel, create_engine

from backend.models.loan import LoanStatus
from backend.models.user import User
from backend.services.loan_list_service import LoanListService

@pytest.fixture(name="db")
def db_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="user")
def user_fixture(db: Session) -> User:
    user = User(
        username="jan_kowalski",
        email="jan@example.com",
        hashed_password="hashed_secret",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_service_exists(db):
    service = LoanListService(db)
    assert service is not None


def test_get_user_loans_returns_list(db, user):
    service = LoanListService(db)
    result = service.get_user_loans(user.id)
    assert isinstance(result, list)


def test_get_all_loans_returns_list(db):
    service = LoanListService(db)
    result = service.get_all_loans()
    assert isinstance(result, list)


def test_get_all_loans_with_status_filter(db):
    service = LoanListService(db)
    result = service.get_all_loans(status=LoanStatus.APPROVED)
    assert isinstance(result, list)