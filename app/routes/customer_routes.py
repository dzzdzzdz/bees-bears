from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_cache.decorator import cache

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

def list_customers_key_builder(func, *args, **kwargs):
    user = kwargs.get("current_user")
    limit = kwargs.get("limit", 10)
    cursor = kwargs.get("cursor")
    return f"list_customers:{user.id if user else 'anon'}:{limit}:{cursor}"

@router.get("", response_model=dict)
@cache(expire=60, key_builder=list_customers_key_builder)
def list_customers(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Customer).filter(Customer.created_by == current_user.id)
    if cursor is not None:
        query = query.filter(Customer.id > cursor)
    query = query.order_by(Customer.id.asc()).limit(limit + 1)
    customers = query.all()

    has_next = len(customers) == limit + 1
    data = customers[:limit]
    next_cursor = data[-1].id if has_next else None

    return {
        "data": [CustomerRead.model_validate(c) for c in data],
        "next_cursor": next_cursor
    }
