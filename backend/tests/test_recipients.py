"""Unit tests for recipient CRUD operations."""

import pytest
from sqlmodel import SQLModel, Session, create_engine

from backend.models.recipient import Recipient
from backend.services.recipient_service import RecipientService


@pytest.fixture(name="db_session")
def session_fixture():
    """Creates an isolated in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_recipient_crud_lifecycle(db_session: Session):
    """Tests full lifecycle: Create, Read, and Delete for a recipient."""
    service = RecipientService(db_session)
    test_user_id = 42

    created = service.add_recipient(
        user_id=test_user_id, name="Mama", account_number="PL00001111"
    )
    assert created.id is not None
    assert created.name == "Mama"
    assert created.account_number == "PL00001111"

    recipients = service.get_recipients(user_id=test_user_id)
    assert len(recipients) == 1
    assert recipients[0].name == "Mama"

    delete_success = service.delete_recipient(
        user_id=test_user_id, recipient_id=created.id
    )
    assert delete_success is True

    assert len(service.get_recipients(user_id=test_user_id)) == 0