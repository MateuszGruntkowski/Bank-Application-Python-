import csv
import io
from datetime import datetime
from sqlmodel import Session, select
from backend.models.transaction import Transaction


class StatementGenerator:
    """Service for generating CSV account statements."""

    def __init__(self, session: Session):
        self.session = session

    def generate_csv(self, account_id: int, start_date: datetime, end_date: datetime) -> str:
        """Downloads transactions and generates the contents of a CSV file."""

        # Database query: select account transactions from a given period
        statement = select(Transaction).where(
            Transaction.account_id == account_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        ).order_by(Transaction.created_at)

        transactions = self.session.exec(statement).all()

        # Preparing a virtual text file in memory
        output = io.StringIO()
        output.write('\ufeff')
        writer = csv.writer(output, delimiter=';')

        # Writing column headings
        writer.writerow(["ID", "Date", "Title", "Amount", "Type"])

        # Loop that writes each row (transaction)
        for t in transactions:
            writer.writerow([
                t.id,
                t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                t.title,
                t.amount,
                t.type
            ])

        # Returning the finished CSV text
        return output.getvalue()
