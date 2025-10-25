from pydantic import BaseModel, EmailStr
from typing import Optional

class LoanOfferBase(BaseModel):
    customer_id: int
    loan_amount: float
    interest_rate: float
    term_months: int

class LoanOfferCreate(LoanOfferBase):
    pass

class LoanOfferRead(LoanOfferBase):
    id: int
    monthly_payment: float

    class Config:
        orm_mode = True