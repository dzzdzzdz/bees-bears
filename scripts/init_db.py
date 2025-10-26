from app.database import engine, Base

from app.models.user import User
from app.models.customer import Customer
from app.models.loanoffer import LoanOffer

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")