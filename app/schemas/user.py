from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=72)]

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True