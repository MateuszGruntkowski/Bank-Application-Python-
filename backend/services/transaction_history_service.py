from sqlmodel import Session, select, desc, asc
from backend.models.transaction import Transaction


class TransactionHistoryService:
    def __init__(self, session: Session):
        self.session = session

    def get_history(self, account_id: int, limit: int = 10, offset: int = 0, sort_order: str = "desc") -> list[Transaction]:
        """
        Downloads transaction history for the given account ID
        including pagination and sorting from the newest to oldest.
        """

        statement = select(Transaction).where(Transaction.account_id == account_id)
        if sort_order.lower() == "asc":
            statement = statement.order_by(asc(Transaction.created_at))
        else:
            statement = statement.order_by(desc(Transaction.created_at))
            statement = statement.offset(offset).limit(limit)

        results = self.session.exec(statement).all()
        return list(results)