from sqlmodel import Session, select
from backend.models.user_profile import UserProfile

class UserProfileService:
    def __init__(self, session: Session):
        self.session = session

    def create_profile(self, profile: UserProfile) -> UserProfile:
        """Saves a new user profile to the database."""
        self.session.add(profile)      # Ddd the profile to the database "waiting room" [cite: 290]
        self.session.commit()           # Save changes permanently [cite: 291]
        self.session.refresh(profile)   # Refresh the object to get e.g. the assigned ID number
        return profile                 # Return the saved profile

    def get_profile(self, user_id: int) -> UserProfile | None:

        pass