from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel


# Possible status
class Status(str, Enum):
    in_progres = "in_progres"
    approved_by_cashier = "approved_by_cashier"
    done = "done"
    paid = "paid"


# Shared properties
class OrderBase(BaseModel):
    user_id: int
    item_id: int


# Properties to receive on item creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on item update
class OrderUpdate(BaseModel):
    status: Status


class OrderInDBBase(BaseModel):
    id: Optional[int] = None
    status: Status

    class Config:
        orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    new_price: Optional[float]
    order_created_date: datetime


# Additional properties stored in DB
class OrderInDB(Order):
    item_created_date: Optional[datetime]
