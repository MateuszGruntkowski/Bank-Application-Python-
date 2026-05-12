import pytest
from sqlmodel import Session, create_engine, SQLModel
from backend.models.user_profile import UserProfile
from backend.services.user_profile_service import UserProfileService


@pytest.fixture
def session():
    """Preparing a temporary database in RAM."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_profile(session: Session):
    service = UserProfileService(session)
    profile = UserProfile(user_id=1, first_name="Jan", last_name="Kowalski", phone="123456789")

    created = service.create_profile(profile)

    assert created.user_id == 1
    assert created.first_name == "Jan"


def test_get_profile_and_not_found(session: Session):
    """Test fetching an existing profile and a non-existent one."""
    service = UserProfileService(session)
    profile = UserProfile(user_id=2, first_name="Anna", last_name="Nowak", phone="987654321")
    service.create_profile(profile)

    fetched = service.get_profile(user_id=2)
    assert fetched is not None
    assert fetched.last_name == "Nowak"

    missing = service.get_profile(user_id=999)
    assert missing is None


def test_update_profile(session: Session):
    """Test updating existing profile data."""
    service = UserProfileService(session)
    profile = UserProfile(user_id=3, first_name="Piotr", last_name="Wisniewski", phone="111222333")
    service.create_profile(profile)

    # We are updating the name itself
    updated = service.update_profile(user_id=3, updated_data={"first_name": "Pawel"})

    assert updated is not None
    assert updated.first_name == "Pawel"
    assert updated.last_name == "Wisniewski"  # The name should remain unchanged
