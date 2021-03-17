from datetime import datetime
from typing import Optional
from fastapi import Path

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Path(default=0.0, ge=0.0)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str
    price: float


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


class ItemUpdateDiscount(BaseModel):
    new_price: float


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    item_created_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    new_price: Optional[float]
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
