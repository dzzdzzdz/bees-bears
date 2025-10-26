# scripts/seed_customers.py
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[0].parent))

from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.services.customer_service import create_customer
from app.schemas.customer import CustomerCreate

fake = Faker()

OWNER_USER_EMAIL = "test@example.com"  # user to own the customers
CUSTOMER_COUNT = 50

def seed_customers(db: Session, user: User, count: int = CUSTOMER_COUNT):
    for _ in range(count):
        name = fake.name()
        email = fake.unique.email()
        customer_data = {
            "name": name,
            "email": email,
            "phone_number": fake.phone_number()
        }
        try:
            customer_in = CustomerCreate(**customer_data)
            create_customer(db, customer_in, user)
        except Exception as e:
            print(f"Skipping duplicate or error: {e}")

if __name__ == "__main__":
    db = SessionLocal()
    user = db.query(User).filter(User.email == OWNER_USER_EMAIL).first()

    if not user:
        raise ValueError(f"User with email {OWNER_USER_EMAIL} not found.")

    seed_customers(db, user, count=CUSTOMER_COUNT)
    db.close()
    print(f"Seeded {CUSTOMER_COUNT} customers for user {OWNER_USER_EMAIL}.")