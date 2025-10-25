from sqlalchemy.orm import Session
from app.models.loanoffer import LoanOffer
from app.schemas.loanoffer import LoanOfferCreate
from app.models.customer import Customer

def create_loan_offer(db: Session, loan_in: LoanOfferCreate) -> LoanOffer:
    customer = db.query(Customer).filter(Customer.id == loan_in.customer_id).first()
    if not customer:
        raise ValueError("Customer does not exist")
    
    monthly_payment = calculate_monthly_payment(
        loan_in.loan_amount,
        loan_in.interest_rate,
        loan_in.term_months
    )

    loan_offer = LoanOffer(
        customer_id=loan_in.customer_id,
        loan_amount=loan_in.loan_amount,
        interest_rate=loan_in.interest_rate,
        term_months=loan_in.term_months,
        monthly_payment=monthly_payment
    )

    db.add(loan_offer)
    db.commit()
    db.refresh(loan_offer)
    return loan_offer

def get_loan_offer_by_id(db: Session, loan_id: int) -> LoanOffer:
    return db.query(LoanOffer).filter(LoanOffer.id == loan_id).first()

def calculate_monthly_payment(amount: float, annual_rate: float, term_months: int) -> float:
    r = annual_rate / 12 / 100
    n = term_months
    if r == 0:
        return round(amount / n, 2)
    M = amount * (r * (1 + r) **n) / ((1 + r) ** n - 1)
    return round(M, 2)