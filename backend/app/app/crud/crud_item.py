from datetime import date
from typing import List

from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

discount_date = date.today() - relativedelta(months=1)

# filter(cast(Item.date, Date) <= discount_date)


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        items = db.query(Item).offset(skip).limit(limit).all()
        new_items = []
        for item in items:
            # print(item.date.date())
            if (
                item.item_created_date.date() <= discount_date and not item.new_price
            ):  # check if discount is already set
                item.new_price = item.price * 0.8  # set 20% discount
            new_items.append(item)
        return new_items


item = CRUDItem(Item)
