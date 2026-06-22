import random
from sqlmodel import Session, select
from datetime import datetime, UTC

from backend.models.transaction import Transaction
from backend.auth.service import AuthService
from backend.database import engine
from backend.models.account import Account
from backend.models.user import User
from backend.models.user_profile import UserProfile
from backend.services.transfer_service import TransferService

try:
    from backend.models.recipient import Recipient
except ImportError:
    Recipient = None


def _generate_account_number(index: int) -> str:
    base = str(index).zfill(26)
    return f"PL{base}"


class DatabaseSeeder:
    def __init__(self, session: Session):
        self.session = session
        self.auth = AuthService(session)
        self.transfer_service = TransferService(session)

    def seed(self):
        if self.session.exec(select(User)).first():
            return

        self._seed_admin()
        users = self._seed_test_users
        self._seed_recipients(users)
        self._seed_transfers(users)

    def _seed_admin(self):
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

    @property
    def _seed_test_users(self) -> list[User]:
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

            account = Account(user_id=user.id, account_number=_generate_account_number(i))
            self.session.add(account)
            self.session.commit()
            self.session.refresh(account)

            imie, nazwisko = name.split("_")

            user_profile = UserProfile(
                user_id=user.id,
                first_name=imie.capitalize(),
                last_name=nazwisko.capitalize(),
                phone=f"+48 111 222 {str(i).zfill(3)}"
            )

            self.session.add(user_profile)
            self.session.commit()

            initial_deposit = Transaction(
                account_id=account.id,
                amount=25000.0,
                title="Initial Income / Salary",
                type="IN",
                created_at=datetime.now(UTC)
            )
            self.session.add(initial_deposit)
            self.session.commit()

            created_users.append(user)

        return created_users

    def _seed_recipients(self, users: list[User]):
        if not Recipient:
            print("Recipient model not imported. Skipping recipients seeding.")
            return

        for user in users:
            others = [u for u in users if u.id != user.id]
            friends = random.sample(others, 2)

            for friend in friends:
                friend_acc = self.session.exec(select(Account).where(Account.user_id == friend.id)).first()
                friend_name = friend.username.replace("_", " ").title()

                recipient = Recipient(
                    user_id=user.id,
                    account_number=friend_acc.account_number,
                    name=f"{friend_name} (Contact)",
                )
                self.session.add(recipient)
        self.session.commit()

    def _seed_transfers(self, users: list[User]):
        titles = [
            "Pizza split", "Movie tickets", "Electricity bill",
            "Netflix subscription", "Gas money", "Birthday gift",
            "Yesterday's lunch", "Apartment rent", "Trip settlement"
        ]

        for user in users:
            sender_acc = self.session.exec(select(Account).where(Account.user_id == user.id)).first()
            others = [u for u in users if u.id != user.id]

            for _ in range(7):
                receiver = random.choice(others)
                receiver_acc = self.session.exec(select(Account).where(Account.user_id == receiver.id)).first()

                amount = round(random.uniform(15.0, 450.0), 2)
                title = random.choice(titles)

                if sender_acc and receiver_acc:
                    try:
                        self.transfer_service.execute_transfer(
                            from_account=sender_acc,
                            to_account_number=receiver_acc.account_number,
                            amount=amount,
                            title=title
                        )
                    except Exception as e:
                        print(f"Error transferring from {user.username}: {e}")


def seed():
    with Session(engine) as db:
        seeder = DatabaseSeeder(db)
        seeder.seed()


if __name__ == "__main__":
    from backend.database import init_db
    init_db()
    seed()
    print("Database seeded successfully with test operations")