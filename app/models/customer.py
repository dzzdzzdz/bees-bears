from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="customers")
    loan_offers = relationship("LoanOffer", back_populates="customer")