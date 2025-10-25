from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)