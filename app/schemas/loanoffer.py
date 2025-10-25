from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class LoanOfferBase(BaseModel):
    customer_id: int
    loan_amount: float
    interest_rate: float
    term_months: int

class LoanOfferCreate(LoanOfferBase):
    customer_id: int
    loan_amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., gt=0)
    term_months: int = Field(..., gt=0)

class LoanOfferRead(LoanOfferBase):
    id: int
    monthly_payment: float

    model_config = ConfigDict(from_attributes=True)