from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.models.user import User

def create_customer(db: Session, customer_in: CustomerCreate, user: User) -> Customer:
    customer = Customer(
        name=customer_in.name,
        email=customer_in.email,
        phone_number=customer_in.phone_number,
        created_by=user.id
    )
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError:
        db.rollback()
        raise ValueError("Customer with this email already exists")
    return customer

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def list_customers(db: Session, user: User, limit: int = 10, cursor: int | None = None) -> List[Customer]:
    query = db.query(Customer).filter(Customer.created_by == user.id)
    if cursor:
        query = query.filter(Customer.id > cursor)
    return query.order_by(Customer.id).limit(limit).all()