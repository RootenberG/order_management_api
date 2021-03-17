from datetime import date
from typing import List
from dateutil.relativedelta import relativedelta


from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.order import Order
from app.models.item import Item
from app.schemas.order import OrderCreate, OrderUpdate
from app.schemas.order import OrderInDB as OrderOrm

discount_date = date.today() - relativedelta(months=1)


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_user(self, db: Session, *, obj_in: User) -> Order:
        return db.query(Order).filter(Order.user_id == obj_in.id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        start_date: date,
        end_date: date
    ) -> List[Order]:

        orders = db.query(
            Order.id,
            Item.title,
            Item.price,
            Item.new_price,
            Item.description,
            Item.item_created_date,
            Order.status,
            Order.order_created_date,
        ).filter(Order.item_id == Item.id)
        if start_date:
            orders = orders.filter(func.date(Order.order_created_date) >= start_date)
        if end_date:
            orders = orders.filter(func.date(Order.order_created_date) <= end_date)
        orders = orders.offset(skip).limit(limit).all()
        new_orders = []
        for order in orders:
            bill = OrderOrm.from_orm(order)
            # print(bill)
            if (
                bill.item_created_date.date() <= discount_date and not bill.new_price
            ):  # check if discount is already set
                bill.new_price = bill.price * 0.8
            new_orders.append(bill)

        return new_orders

    def in_progres(self, db: Session, *, obj_in: User) -> bool:
        order = db.query(Order).filter(Order.user_id == obj_in.id).first()
        if not order:
            return False
        return order.status in {
            "in_progres",
            "approved_by_cashier",
            "approved_by_seller",
        }


order = CRUDOrder(Order)
