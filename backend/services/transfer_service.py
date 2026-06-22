"""Transfer service - handles internal transfers between accounts."""

from sqlmodel import Session, select

from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType
from backend.services.balance_calculator import BalanceCalculator
from backend.services.transaction_limit_service import TransactionLimitService

class InsufficientFundsError(Exception):
    """Raised when the sender does not have enough funds."""
    pass


class AccountNotFoundError(Exception):
    """Raised when the specified account does not exist."""
    pass


class TransferService:
    """Service responsible for executing internal transfers between accounts."""

    def __init__(self, session: Session):
        self.session = session
        self.balance_calculator = BalanceCalculator()

    def execute_transfer(self, from_account: Account, to_account_number: str, amount: float, title: str) -> None:
        """
        Execute an internal transfer between two accounts.

        Creates two Transaction records in a single DB transaction:
        - OUT record for the sender
        - IN record for the receiver

        Args:
            from_account (Account): The sender's account object.
            to_account_number (str): The recipient's account number.
            amount (float): The amount to transfer (must be > 0).
            title (str): The transfer title/description.

        Raises:
            AccountNotFoundError: If the recipient account does not exist.
            InsufficientFundsError: If the sender has insufficient funds.
        """
        # Verify recipient exists
        statement = select(Account).where(Account.account_number == to_account_number)
        to_account = self.session.exec(statement).first()

        if to_account is None:
            raise AccountNotFoundError(f"Account with number '{to_account_number}' not found.")

        # Verify sender has sufficient funds
        balance = self.balance_calculator.get_balance(from_account.id, self.session)
        if balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: {balance:.2f}, requested: {amount:.2f}."
            )

        # Verify senders transaction limits
        limit_service = TransactionLimitService(self.session)
        limit_service.validate_transfer_limits(from_account, amount)

        # Execute transfer as a single DB transaction
        try:
            outgoing = Transaction(
                account_id=from_account.id,
                amount=amount,
                title=title,
                type=TransactionType.OUT,
            )
            incoming = Transaction(
                account_id=to_account.id,
                amount=amount,
                title=title,
                type=TransactionType.IN,
            )

            self.session.add(outgoing)
            self.session.add(incoming)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise