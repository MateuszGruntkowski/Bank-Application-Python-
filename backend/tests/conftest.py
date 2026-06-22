import pytest
from unittest.mock import MagicMock

@pytest.fixture
def db():
    mock_db = MagicMock()
    mock_db.exec.return_value.all.return_value = []
    return mock_db

@pytest.fixture
def user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test_user"
    return mock_user