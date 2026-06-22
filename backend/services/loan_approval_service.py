from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime, timezone

from backend.models.loan import Loan, LoanStatus
from backend.models.transaction import Transaction
from backend.models.account import Account


class LoanApprovalService:
    """Service for approving or rejecting loan applications."""

    def __init__(self, session: Session):
        self.session = session

    def approve_loan(self, loan_id: int) -> Loan:
        # looking for an application in the database
        loan = self.session.get(Loan, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Wniosek kredytowy nie istnieje.")

        # check whether the application is still waiting for a decision
        if loan.status != LoanStatus.PENDING:
            raise HTTPException(status_code=400, detail="Ten wniosek został już rozpatrzony.")

        # looking for this customer's bank account (to transfer money to him)
        account = self.session.exec(
            select(Account).where(Account.user_id == loan.user_id)
        ).first()

        if not account:
            raise HTTPException(status_code=404, detail="Użytkownik nie posiada konta bankowego.")

        # create a new transaction (Loan disbursement to account)
        transaction = Transaction(
            account_id=account.id,
            amount=loan.amount,
            title="Wypłata środków z kredytu",
            type="IN"  # Money arriving at your account
        )
        self.session.add(transaction)

        # updating the application
        loan.status = LoanStatus.APPROVED
        loan.updated_at = datetime.now(timezone.utc)
        self.session.add(loan)

        # saving
        self.session.commit()
        self.session.refresh(loan)

        return loan

    def reject_loan(self, loan_id: int, reason: str) -> Loan:
        # search for the application in the database
        loan = self.session.get(Loan, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Wniosek kredytowy nie istnieje.")

        # check whether the application is still waiting for a decision
        if loan.status != LoanStatus.PENDING:
            raise HTTPException(status_code=400, detail="Ten wniosek został już rozpatrzony.")

        # reject the application and record the reason
        loan.status = LoanStatus.REJECTED
        loan.rejection_reason = reason
        loan.updated_at = datetime.now(timezone.utc)

        self.session.add(loan)
        self.session.commit()
        self.session.refresh(loan)

        return loan
