from sqlmodel import Session, select
from backend.models.transaction import Transaction, TransactionType


class BalanceCalculator:
    """
    Service class responsible for financial calculations related to user accounts.
    """

    def get_balance(self, account_id: int, session: Session) -> float:
        """
        Calculates the current balance for a specific account.

        Args:
            account_id (int): The ID of the account to calculate the balance for.
            session (Session): The active database session.

        Returns:
            float: The calculated balance (sum of INs minus sum of OUTs).
        """

        statement = select(Transaction).where(Transaction.account_id == account_id)
        transactions = session.exec(statement).all()

        balance = 0.0

        for txn in transactions:
            if txn.type == TransactionType.IN:
                balance += txn.amount
            elif txn.type == TransactionType.OUT:
                balance -= txn.amount

        return balance