from datetime import date
from typing import List

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session


from app.crud.base import CRUDBase
from app.models.bill import Bill
from app.models.order import Order
from app.models.user import User
from app.models.item import Item

from app.schemas.bill import BillCreate, BillUpdate
from app.schemas.bill import BillInDB as BillOrm


discount_date = date.today() - relativedelta(months=1)

# filter(cast(Item.date, Date) <= discount_date)


class CRUDItem(CRUDBase[Bill, BillCreate, BillUpdate]):
    def get_by_order(self, db: Session, *, order: Order) -> Bill:
        bill = db.query(Bill).filter(Bill.order_id == order.id).first()
        return bill

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        bills = (
            db.query(
                Bill.id,
                Bill.status,
                Item.title,
                Item.description,
                Item.price,
                Item.new_price,
                Order.order_created_date,
                Bill.bill_created_date,
                Item.item_created_date,
            )
            .filter(Bill.order_id == Order.id)
            .filter(Order.item_id == Item.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        # print(bills)

        new_bills = []
        for bill in bills:
            bill = BillOrm.from_orm(bill)
            print(bill)
            if (
                bill.item_created_date.date() <= discount_date and not bill.new_price
            ):  # check if discount is already set
                bill.new_price = bill.price * 0.8
            new_bills.append(bill)
        return new_bills

    def get_multi_by_user(
        self, db: Session, *, user: User, skip: int = 0, limit: int = 100
    ) -> List[BillOrm]:
        bills = (
            db.query(
                Bill.id,
                Bill.status,
                Item.title,
                Item.description,
                Item.price,
                Item.new_price,
                Order.order_created_date,
                Bill.bill_created_date,
                Item.item_created_date,
            )
            .filter(Order.user_id == user.id)
            .filter(Order.item_id == Item.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        new_bills = []
        for bill in bills:
            bill = BillOrm.from_orm(bill)
            print(bill)
            if (
                bill.item_created_date.date() <= discount_date and not bill.new_price
            ):  # check if discount is already set
                bill.new_price = bill.price * 0.8
            new_bills.append(bill)
        return new_bills


bill = CRUDItem(Bill)
