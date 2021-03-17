import datetime
from sqlalchemy import DateTime, Column, Integer, ForeignKey, String, Float

from app.db.base_class import Base


class Bill(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    status = Column(String, default="created")
    bill_created_date = Column(DateTime, default=datetime.datetime.now())