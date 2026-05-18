from sqlmodel import Session, select
from backend.models.user import User
from backend.seeder import DatabaseSeeder


def test_seeder_creates_five_users_and_admin(db_session: Session):
    """Test if seeder populates the database with exactly 6 users."""
    seeder = DatabaseSeeder(db_session)
    seeder.seed()

    users = db_session.exec(select(User)).all()
    assert len(users) == 6


def test_seeder_idempotent(db_session: Session):
    """Test if running seeder twice does not duplicate records."""
    seeder = DatabaseSeeder(db_session)

    seeder.seed()
    seeder.seed()

    users = db_session.exec(select(User)).all()
    assert len(users) == 6