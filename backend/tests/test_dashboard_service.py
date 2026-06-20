from unittest.mock import MagicMock
from backend.services.dashboard_service import DashboardService


def test_get_dashboard():
    """Test DashboardService.get_dashboard using mocked DB session."""

    session = MagicMock()
    service = DashboardService(session)

    mock_txn = MagicMock()
    mock_txn.type = "IN"
    mock_txn.amount = 100.0

    mock_account = MagicMock()
    mock_account.user_id = 1
    mock_account.__getitem__.side_effect = lambda key: 1 if key == "user_id" else MagicMock()

    session.exec.return_value.all.return_value = [mock_txn, mock_txn, mock_txn, mock_txn, mock_txn]

    session.exec.return_value.first.return_value = mock_account

    result = service.get_dashboard(user_id=1)

    assert result["account"]["user_id"] == 1
    assert result["balance"] is not None
    assert len(result["recent_transactions"]) == 5
    assert result["unread_notifications"] == 0