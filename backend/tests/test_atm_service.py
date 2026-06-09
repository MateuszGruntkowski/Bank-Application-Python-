import pytest
from unittest.mock import MagicMock
from backend.services.atm_service import ATMService


def test_deposit():
    session = MagicMock()
    service = ATMService(session)

    service.deposit(1, 100)

    assert session.add.called
    assert session.commit.called


def test_withdraw_insufficient_funds():
    session = MagicMock()
    service = ATMService(session)

    service.balance_calculator.get_balance = MagicMock(return_value=0)

    with pytest.raises(ValueError):
        service.withdraw(1, 100)
