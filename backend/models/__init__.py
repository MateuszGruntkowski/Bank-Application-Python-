"""Models package. Import all models here so they are registered with SQLModel."""

from backend.models.user import User
from backend.models.account import Account
from .loan import Loan

__all__ = ["User", "Account"]
