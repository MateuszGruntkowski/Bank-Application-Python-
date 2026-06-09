import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from backend.models.transaction import Transaction, TransactionType
from backend.services.balance_calculator import BalanceCalculator
from backend.seeder import DatabaseSeeder
from backend.models.user import User
from backend.models.account import Account

@pytest.fixture(name="session")
def session_fixture():
    """
    Creates an in-memory SQLite database strictly for testing purposes.
    It's completely isolated from real bank.db file.
    """
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_get_balance_calculates_correctly(session: Session):
    """
    Test to verify if BalanceCalculator accurately sums INs and subtracts OUTs.
    """
    txn1 = Transaction(account_id=1, amount=1000.0, title="Salary", type=TransactionType.IN)
    txn2 = Transaction(account_id=1, amount=250.0, title="Groceries", type=TransactionType.OUT)
    txn3 = Transaction(account_id=2, amount=500.0, title="Different Account", type=TransactionType.IN)

    session.add(txn1)
    session.add(txn2)
    session.add(txn3)
    session.commit()

    calculator = BalanceCalculator()
    balance = calculator.get_balance(account_id=1, session=session)

    assert balance == 750.0

def test_balance_calculator_with_seeder(session: Session):
    """
    Test to verify if BalanceCalculator accurately sums INs and subtracts OUTs.
    """
    seeder = DatabaseSeeder(session)
    seeder.seed()

    jan = session.exec(select(User).where(User.username == "jan_kowalski")).first()
    jan_account = session.exec(select(Account).where(Account.user_id == jan.id)).first()

    calculator = BalanceCalculator()
    balance = calculator.get_balance(account_id=jan_account.id, session=session)

    assert balance == 0.0