from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.loanoffer import LoanOfferCreate, LoanOfferRead
from app.services.loan_service import create_loan_offer, get_loan_offer_by_id
from app.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/loanoffers", tags=["loanoffers"])

@router.post("", response_model=LoanOfferRead, status_code=status.HTTP_201_CREATED)
def post_loan_offer(
    loan_in: LoanOfferCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        loan_offer = create_loan_offer(db, loan_in)
        return loan_offer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{loan_id}", response_model=LoanOfferRead)
def get_loan_offer(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    loan_offer = get_loan_offer_by_id(db, loan_id)
    if not loan_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan offer not found")
    return loan_offer