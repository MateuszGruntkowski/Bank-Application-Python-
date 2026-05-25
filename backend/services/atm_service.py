from sqlmodel import Session

from backend.models.transaction import Transaction, TransactionType
from backend.services.balance_calculator import BalanceCalculator

class ATMService:
    """Service integrating ATM operations with the banking system."""

    def __init__(self, session: Session):
        self.session = session
        self.balance_calculator = BalanceCalculator()

    def get_balance(self, account_id: int) -> float:
        """Returns current account balance."""
        return self.balance_calculator.get_balance(account_id, self.session)

    def deposit(self, account_id: int, amount: float) -> None:
        """Creates incoming transaction (IN)."""
        transaction = Transaction(
            account_id=account_id,
            amount=amount,
            title="ATM deposit",
            type=TransactionType.IN,
        )
        self.session.add(transaction)
        self.session.commit()

    def withdraw(self, account_id: int, amount: float) -> None:
        """Creates outgoing transaction (OUT) after balance validation."""

        balance = self.balance_calculator.get_balance(account_id, self.session)

        if balance < amount:
            raise ValueError("Insufficient funds")

        transaction = Transaction(
            account_id=account_id,
            amount=amount,
            title="ATM withdrawal",
            type=TransactionType.OUT,
        )
        self.session.add(transaction)
        self.session.commit()