from sqlmodel import Session, select
from backend.models.user_profile import UserProfile


class UserProfileService:
    """Service handling business logic for user profiles."""

    def __init__(self, session: Session):
        self.session = session

    def create_profile(self, profile: UserProfile) -> UserProfile:
        """Saves a new user profile to the database."""
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def get_profile(self, user_id: int) -> UserProfile | None:
        """Retrieves a user profile by user_id."""
        statement = select(UserProfile).where(UserProfile.user_id == user_id)
        return self.session.exec(statement).first()

    def update_profile(self, user_id: int, updated_data: dict) -> UserProfile | None:
        """Updates an existing user profile."""
        profile = self.get_profile(user_id)
        if profile:
            # We only update the fields that were passed in updated_data
            for key, value in updated_data.items():
                setattr(profile, key, value)
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
        return profile
