"""Credit Scoring Service for evaluating user loan eligibility."""

from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select
from backend.models.account import Account
from backend.models.transaction import Transaction
from backend.services.balance_calculator import BalanceCalculator

class CreditScoringService:
    """Service to calculate credit score and recommendation for a user."""
    
    @staticmethod
    def calculate_score(user_id: int, db: Session) -> dict:
        """
        Calculate credit score based on user finances:
        - transactions per month
        - average balance
        - account age
        - absence of debts
        """
        account = db.exec(select(Account).where(Account.user_id == user_id)).first()
        
        if not account:
            return {"score": 0, "recommendation": "REJECT"}
            
        now = datetime.now(timezone.utc)
        
        # Ensure account.created_at is timezone-aware
        created_at = account.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            
        account_age_days = (now - created_at).days
        account_age_months = max(1, account_age_days // 30)
        
        # Get transactions from the last 30 days
        thirty_days_ago = now - timedelta(days=30)
        thirty_days_ago_naive = thirty_days_ago.replace(tzinfo=None) # SQLite might not support timezone

        transactions_30d = db.exec(
            select(Transaction).where(
                Transaction.account_id == account.id
            )
        ).all()
        
        transactions_per_month = 0
        for tx in transactions_30d:
            tx_time = tx.created_at
            if tx_time.tzinfo is None:
                 tx_time = tx_time.replace(tzinfo=timezone.utc)
            if tx_time >= thirty_days_ago:
                 transactions_per_month += 1

        
        balance_calculator = BalanceCalculator()
        current_balance = balance_calculator.get_balance(account.id, db)
        average_balance = current_balance
        
        has_debts = current_balance < 0
        
        score = 0
        

        score += min(30, account_age_months * 2)
        
        if transactions_per_month > 20:
            score += 30
        elif transactions_per_month > 10:
            score += 20
        elif transactions_per_month > 0:
            score += 10
            
        if average_balance > 5000:
            score += 40
        elif average_balance > 2000:
            score += 30
        elif average_balance > 1000:
            score += 20
        elif average_balance > 0:
            score += 10
            
        if has_debts:
            score -= 50
            
        recommendation = "APPROVE" if score >= 60 and not has_debts else "REJECT"
        
        score = max(0, min(100, int(score)))
        
        return {
            "score": score,
            "recommendation": recommendation
        }
