"""Admin router - endpoints for admin operations."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import require_admin
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


class RejectRequest(BaseModel):
    """Schema for rejecting a loan with reason."""
    reason: str


class ChargeFeeRequest(BaseModel):
    """Schema for charging account fees."""
    amount: float


class ReversalRequest(BaseModel):
    """Schema for reversing a transaction."""
    reason: str


@router.get("/loans")
def get_all_loans(status: str = "", page: int = 1, per_page: int = 10, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get all loan applications with optional status filter."""
    # TODO: Implement using LoanListService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for LoanListService")


@router.post("/loans/{loan_id}/approve")
def approve_loan(loan_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Approve a loan application."""
    # TODO: Implement using LoanApprovalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for LoanApprovalService")


@router.post("/loans/{loan_id}/reject")
def reject_loan(loan_id: int, request: RejectRequest, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Reject a loan application."""
    # TODO: Implement using LoanApprovalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for LoanApprovalService")


@router.get("/scoring/{user_id}")
def get_credit_score(user_id: int, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get credit score for a specific user."""
    # TODO: Implement using CreditScoringService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for CreditScoringService")


@router.post("/transactions/{transaction_id}/reverse")
def reverse_transaction(transaction_id: int, request: ReversalRequest, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Reverse a transaction by creating a compensating entry."""
    # TODO: Implement using TransactionReversalService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for TransactionReversalService")


@router.post("/execute-standing-orders")
def execute_standing_orders(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Execute all pending standing orders."""
    # TODO: Implement using StandingOrderService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for StandingOrderService")


@router.post("/charge-fees")
def charge_fees(request: ChargeFeeRequest, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Charge account maintenance fees to all active accounts."""
    # TODO: Implement using AccountFeeService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for AccountFeeService")


@router.get("/stats")
def get_bank_statistics(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get aggregated bank statistics."""
    # TODO: Implement using BankStatisticsService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for BankStatisticsService")


@router.get("/export")
def export_bank_data(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Export anonymized bank report as JSON."""
    # TODO: Implement using DataExportService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for DataExportService")
