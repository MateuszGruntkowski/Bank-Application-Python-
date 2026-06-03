import pytest
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, select
from backend.models.user import User
from backend.models.account import Account
from backend.models.transaction import Transaction
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

    # Poprawione typy transakcji: 'IN' oraz 'OUT'
    t1 = Transaction(account_id=jan_account.id, amount=10.0, title="T1_Old", type="IN", created_at=datetime(2026, 6, 1, 10, 0, 0))
    t2 = Transaction(account_id=jan_account.id, amount=20.0, title="T2_Mid", type="OUT", created_at=datetime(2026, 6, 2, 10, 0, 0))
    t3 = Transaction(account_id=jan_account.id, amount=30.0, title="T3_New", type="IN", created_at=datetime(2026, 6, 3, 10, 0, 0))

    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.commit()

    service = TransactionHistoryService(session)

    # A) Testing DESC
    history_desc = service.get_history(account_id=jan_account.id, sort_order="desc")
    assert history_desc[0].title == "T3_New"

    # B) Testing ASC
    history_asc = service.get_history(account_id=jan_account.id, sort_order="asc")
    assert history_asc[0].title == "T1_Old"

    # C) Testing paginating (page 1, 2 records per page)
    page_1 = service.get_history(account_id=jan_account.id, limit=2, offset=0, sort_order="desc")
    assert len(page_1) == 2
    assert page_1[0].title == "T3_New"
    assert page_1[1].title == "T2_Mid"

    # D) Testing paginating (page 2, 2 records per page)
    page_2 = service.get_history(account_id=jan_account.id, limit=2, offset=2, sort_order="desc")
    assert len(page_2) == 1  #Only one left
    assert page_2[0].title == "T1_Old"