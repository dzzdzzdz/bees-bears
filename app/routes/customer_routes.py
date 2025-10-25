from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.customer import CustomerCreate, CustomerRead
from app.models.customer import Customer
from app.services.customer_service import create_customer, get_customer_by_id
from app.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def post_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        customer = create_customer(db, customer_in, current_user)
        return customer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer = get_customer_by_id(db, customer_id)
    if not customer or customer.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer