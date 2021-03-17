import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, Float

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    new_price = Column(Float)
    item_created_date = Column(DateTime, default=datetime.datetime.now)
