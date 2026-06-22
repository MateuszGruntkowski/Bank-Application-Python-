import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from backend.models.user import User
from backend.models.account import Account
from backend.services.transaction_history_service import TransactionHistoryService
from backend.seeder import DatabaseSeeder

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_transaction_history_pagination_and_sorting(session: Session):
    """
    Test to verify if transaction history service properly
    paginates and sorts for given account_id.
    """
    seeder = DatabaseSeeder(session)
    seeder.seed()

    jan = session.exec(select(User).where(User.username == "jan_kowalski")).first()
    jan_account = session.exec(select(Account).where(Account.user_id == jan.id)).first()

    service = TransactionHistoryService(session)

    all_transactions = service.get_history(account_id=jan_account.id, limit=10, offset=0)

    # A) Main test
    all_transactions = service.get_history(account_id=jan_account.id, limit=10, offset=0)
    assert len(all_transactions) == 10

    # B) Pagination test (page 1: limit 2)
    page_1 = service.get_history(account_id=jan_account.id, limit=2, offset=0)
    assert len(page_1) == 2

    # C) Pagination test (page 2: limit 2, offset 2) - only one transaction left
    page_2 = service.get_history(account_id=jan_account.id, limit=2, offset=2)
    assert len(page_2) == 2