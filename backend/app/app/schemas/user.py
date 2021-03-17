from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


# Possible users
class Permissions(str, Enum):
    user = "user"
    cashier = "cashier"
    seller = "seller"
    accountant = "accountant"


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    permissions: Permissions


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    permissions: Permissions


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    permissions: Optional[Permissions]



class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
