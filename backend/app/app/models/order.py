import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String

from app.db.base_class import Base


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    item_id = Column(Integer, ForeignKey("item.id"))
    status = Column(String, default="in_progres")
    order_created_date = Column(DateTime, default=datetime.datetime.now())
