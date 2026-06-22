import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone

from backend.services.scoring import CreditScoringService
from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType

def test_calculate_score_no_account():
    """Test score when user has no account."""
    db_mock = MagicMock()
    db_mock.exec.return_value.first.return_value = None
    
    result = CreditScoringService.calculate_score(1, db_mock)
    
    assert result["score"] == 0
    assert result["recommendation"] == "REJECT"

@patch('backend.services.scoring.BalanceCalculator')
def test_calculate_score_with_debts(MockBalanceCalculator):
    """Test score when user has debts (balance < 0)."""
    db_mock = MagicMock()
    mock_account = Account(id=1, user_id=5, account_number="123", created_at=datetime.now(timezone.utc) - timedelta(days=90))
    
    db_mock.exec.return_value.first.return_value = mock_account
    db_mock.exec.return_value.all.return_value = [] # no transactions
    
    instance = MockBalanceCalculator.return_value
    instance.get_balance.return_value = -500.0 # debt
    
    result = CreditScoringService.calculate_score(5, db_mock)
    
    assert result["recommendation"] == "REJECT"
    assert result["score"] < 60

@patch('backend.services.scoring.BalanceCalculator')
def test_calculate_score_good_finances(MockBalanceCalculator):
    """Test score when user has good finances."""
    db_mock = MagicMock()
    mock_account = Account(id=1, user_id=2, account_number="123", created_at=datetime.now(timezone.utc) - timedelta(days=300))
    
    db_mock.exec.return_value.first.return_value = mock_account
    
    recent_tx = Transaction(account_id=1, amount=100.0, title="tx", type=TransactionType.IN, created_at=datetime.now(timezone.utc) - timedelta(days=5))
    db_mock.exec.return_value.all.return_value = [recent_tx] * 15
    
    instance = MockBalanceCalculator.return_value
    instance.get_balance.return_value = 2500.0 # > 2000 -> 30 pts
    
    result = CreditScoringService.calculate_score(2, db_mock)
    
    assert result["score"] == 70
    assert result["recommendation"] == "APPROVE"

@patch('backend.services.scoring.BalanceCalculator')
def test_calculate_score_poor_finances(MockBalanceCalculator):
    """Test score when user has poor finances."""
    db_mock = MagicMock()
    mock_account = Account(id=1, user_id=3, account_number="123", created_at=datetime.now(timezone.utc))
    db_mock.exec.return_value.first.return_value = mock_account
    
    recent_tx = Transaction(account_id=1, amount=10.0, title="tx", type=TransactionType.IN, created_at=datetime.now(timezone.utc))
    db_mock.exec.return_value.all.return_value = [recent_tx] * 5
    
    instance = MockBalanceCalculator.return_value
    instance.get_balance.return_value = 100.0 # > 0 -> 10 pts
    
    result = CreditScoringService.calculate_score(3, db_mock)
    
    assert result["score"] == 22
    assert result["recommendation"] == "REJECT"
