"""External transfer service - handles transfers to accounts outside the system."""

from sqlmodel import Session

from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType
from backend.services.balance_calculator import BalanceCalculator
from backend.services.transfer_service import InsufficientFundsError


class ExternalTransferService:
    """Service responsible for executing transfers to external (outside system) accounts."""

    def __init__(self, session: Session):
        self.session = session
        self.balance_calculator = BalanceCalculator()

    def execute_transfer(self, from_account: Account, to_account_number: str, amount: float, title: str) -> None:
        """
        Execute a transfer to an external account.

        Creates a single OUT_EXTERNAL Transaction record for the sender.
        No verification of recipient — external accounts are outside the system.

        Args:
            from_account (Account): The sender's account object.
            to_account_number (str): The recipient's external account number.
            amount (float): The amount to transfer (must be > 0).
            title (str): The transfer title/description.

        Raises:
            InsufficientFundsError: If the sender has insufficient funds.
        """
        if amount <= 0:
            raise ValueError(f"Transfer amount must be positive, got: {amount}.")

        balance = self.balance_calculator.get_balance(from_account.id, self.session)
        if balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: {balance:.2f}, requested: {amount:.2f}."
            )

        try:
            outgoing = Transaction(
                account_id=from_account.id,
                amount=amount,
                title=title,
                type=TransactionType.OUT_EXTERNAL,
            )
            self.session.add(outgoing)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise