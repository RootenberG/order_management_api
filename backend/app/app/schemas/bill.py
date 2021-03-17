from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class Status(str, Enum):
    created = "created"
    paid = "paid"


# Shared properties
class BillBase(BaseModel):
    order_id: int


# Properties to receive on item creation
class BillCreate(BillBase):
    pass


# Properties to receive on item update
class BillUpdate(BaseModel):
    status: Status


# Properties shared by models stored in DB
class BillInDBBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Bill(BillInDBBase):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    new_price: Optional[float]
    status: Optional[Status]
    order_created_date: Optional[datetime]
    bill_created_date: Optional[datetime]


class BillInDB(Bill):
    item_created_date: Optional[datetime]