import pytest
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, create_engine, SQLModel

from backend.models.transaction import Transaction
from backend.services.statement_generator import StatementGenerator


@pytest.fixture
def session():
    """Preparing a temporary database in RAM."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_generate_csv_statement(session: Session):
    # Preparing test data
    now = datetime.now(timezone.utc)

    # Two transactions within the selected time frame
    t1 = Transaction(account_id=1, amount=100.0, title="Wypłata z bankomatu", type="IN",
                     created_at=now - timedelta(days=2))
    t2 = Transaction(account_id=1, amount=15.50, title="Kawa", type="OUT", created_at=now - timedelta(days=5))

    # One old transaction (out of scope - should not be included in the statement!)
    t3 = Transaction(account_id=1, amount=500.0, title="Stary Przelew", type="IN", created_at=now - timedelta(days=30))

    session.add_all([t1, t2, t3])
    session.commit()

    # Starting generator
    generator = StatementGenerator(session)
    date_from = now - timedelta(days=10)
    date_to = now

    csv_data = generator.generate_csv(account_id=1, start_date=date_from, end_date=date_to)

    # Verification
    assert "ID;Date;Title;Amount;Type" in csv_data  # Checks if column headers are present
    assert "Wypłata z bankomatu" in csv_data  # Checks if a new transaction has been found
    assert "Kawa" in csv_data  # Checks if it found a second new transaction
    assert "Stary Przelew" not in csv_data  # Makes sure the old transaction is ignored
