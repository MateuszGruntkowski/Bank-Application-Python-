from unittest.mock import MagicMock
from backend.services.dashboard_service import DashboardService


def test_get_dashboard():
    """Test DashboardService.get_dashboard using mocked DB session."""

    session = MagicMock()
    service = DashboardService(session)

    session.exec.return_value.all.return_value = ["t1", "t2", "t3", "t4", "t5"]

    result = service.get_dashboard(user_id=1)

    assert result["account"]["user_id"] == 1
    assert result["balance"] is not None
    assert len(result["last_transactions"]) == 5
    assert result["unread_notifications"] == 0