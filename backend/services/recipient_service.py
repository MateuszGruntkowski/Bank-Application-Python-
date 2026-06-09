"""Service handling CRUD operations for saved recipients."""

from sqlmodel import Session, select
from backend.models.recipient import Recipient


class RecipientService:
    """Service responsible for managing saved recipients in the database."""

    def __init__(self, session: Session):
        self.session = session

    def add_recipient(self, user_id: int, name: str, account_number: str) -> Recipient:
        """Saves a new recipient for the given user."""
        recipient = Recipient(user_id=user_id, name=name, account_number=account_number)
        self.session.add(recipient)
        self.session.commit()
        self.session.refresh(recipient)
        return recipient

    def get_recipients(self, user_id: int) -> list[Recipient]:
        """Returns a list of all saved recipients for the given user."""
        statement = select(Recipient).where(Recipient.user_id == user_id)
        return self.session.exec(statement).all()

    def delete_recipient(self, user_id: int, recipient_id: int) -> bool:
        """Deletes a saved recipient if it belongs to the user."""
        statement = select(Recipient).where(
            Recipient.id == recipient_id, Recipient.user_id == user_id
        )
        recipient = self.session.exec(statement).first()

        if not recipient:
            return False

        self.session.delete(recipient)
        self.session.commit()
        return True