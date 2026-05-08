import pytest
from sqlmodel import Session, create_engine, SQLModel
from backend.models.user_profile import UserProfile
from backend.services.user_profile_service import UserProfileService

@pytest.fixture
def session():
    """Przygotowanie tymczasowej bazy danych w pamięci RAM."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_profile(session: Session):
    service = UserProfileService(session)
    profile = UserProfile(user_id=1, phone_number="123", address="ul. Test", city="Poznan")
    
    created = service.create_profile(profile)
    
    assert created.user_id == 1  # Test sprawdzi, czy dane się zapisały