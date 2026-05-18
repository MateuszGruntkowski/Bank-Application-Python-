"""
Database seeder - creates initial admin user and test data.
Run once on first startup to populate the database.
"""

from decimal import Decimal
from sqlmodel import Session, select

from backend.auth.service import AuthService
from backend.database import engine
from backend.models.account import Account
from backend.models.user import User
from backend.services.transfer_service import TransferService


def _generate_account_number(index: int) -> str:
    """Generate a deterministic account number for seeding."""
    base = str(index).zfill(26)
    return f"PL{base}"


class DatabaseSeeder:
    """Service for seeding 5 test users and generating transfer history."""

    def __init__(self, session: Session):
        self.session = session
        self.auth = AuthService(session)
        self.transfer_service = TransferService(session)

    def seed(self):
        """Executes the seeding process."""
        if self.session.exec(select(User)).first():
            return

        self._seed_admin()
        users = self._seed_test_users()
        self._seed_transfers(users)

    def _seed_admin(self):
        """Creates the admin user from the original code."""
        admin = User(
            username="admin",
            email="admin@bank.io",
            hashed_password=self.auth.hash_password("admin"),
            is_admin=True,
        )
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)

        self.session.add(Account(user_id=admin.id, account_number=_generate_account_number(1)))
        self.session.commit()

    def _seed_test_users(self) -> list[User]:
        """Creates exactly 5 test users as required by task 3."""
        users_data = [
            ("jan_kowalski", "jan@bank.io"),
            ("anna_nowak", "anna@bank.io"),
            ("tomasz_test", "tomasz@bank.io"),
            ("ewa_test", "ewa@bank.io"),
            ("michal_test", "michal@bank.io")
        ]

        created_users = []
        for i, (name, email) in enumerate(users_data, start=2):
            user = User(
                username=name,
                email=email,
                hashed_password=self.auth.hash_password("password123"),
            )
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            self.session.add(Account(user_id=user.id, account_number=_generate_account_number(i)))
            self.session.commit()
            created_users.append(user)

        return created_users

    def _seed_transfers(self, users: list[User]):
        """Uses TransferService to generate transfer history between test users."""
        for i in range(len(users)):
            sender = users[i]
            receiver = users[(i + 1) % len(users)]

            sender_acc = self.session.exec(select(Account).where(Account.user_id == sender.id)).first()
            receiver_acc = self.session.exec(select(Account).where(Account.user_id == receiver.id)).first()

            if sender_acc and receiver_acc:
                try:
                    self.transfer_service.execute_transfer(
                        from_account=sender_acc.account_number,
                        to_account=receiver_acc.account_number,
                        amount=Decimal("100.00"),
                        title=f"Test transfer from {sender.username}"
                    )
                except Exception as e:
                    pass


def seed():
    """Populate the database with initial data if empty."""
    with Session(engine) as db:
        seeder = DatabaseSeeder(db)
        seeder.seed()


if __name__ == "__main__":
    from backend.database import init_db
    init_db()
    seed()
    print("Database seeded successfully.")
