from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class LoanOffer(Base):
    __tablename__ = "loan_offers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    monthly_payment = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="loan_offers")