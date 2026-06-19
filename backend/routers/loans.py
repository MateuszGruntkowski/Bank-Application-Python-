"""Loans router - endpoints for loan applications, approval, repayment."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.auth import get_current_user, require_admin
from backend.database import get_db
from backend.models.user import User
from backend.services.loan_application_service import LoanApplicationService, LoanApplicationError
from backend.services.loan_list_service import LoanListService

router = APIRouter(prefix="/loans", tags=["Loans"])


class LoanApplicationRequest(BaseModel):
    """Schema for applying for a loan."""
    amount: float


class LoanRepaymentRequest(BaseModel):
    """Schema for repaying a loan."""
    amount: float


@router.post("/apply", status_code=201)
def apply_for_loan(
        request: LoanApplicationRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Submit a loan application for the authenticated user."""
    service = LoanApplicationService(db)
    try:
        loan = service.apply(user=current_user, amount=request.amount)
    except LoanApplicationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {
        "message": "Loan application submitted successfully.",
        "loan_id": loan.id,
        "amount": loan.amount,
        "status": loan.status.value,
        "created_at": loan.created_at.isoformat(),
    }

@router.get("/me")
def get_my_loans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's loans."""
    # TODO: Implement using LoanListService
    return LoanListService(db).get_user_loans(current_user.id)


@router.get("/{loan_id}/schedule")
def get_loan_schedule(loan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get repayment schedule for a specific loan."""
    # TODO: Implement using RepaymentScheduleService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for RepaymentScheduleService")


@router.post("/{loan_id}/repay")
def repay_loan(loan_id: int, request: LoanRepaymentRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Make a loan repayment (full or partial)."""
    # TODO: Implement using LoanRepaymentService
    raise HTTPException(status_code=501, detail="Not implemented - waiting for LoanRepaymentService")
