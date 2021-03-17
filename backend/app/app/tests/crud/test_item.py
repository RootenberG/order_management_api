import random
from sqlalchemy.orm import Session

from app import crud
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random.randint(0, 999)
    item_in = ItemCreate(title=title, description=description, price=price)
    item = crud.item.create(db=db, obj_in=item_in)
    assert item.title == title
    assert item.description == description
    assert item.price == price
    # assert item.owner_id == user.id


def test_get_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random.randint(0, 999)
    item_in = ItemCreate(title=title, description=description, price=price)
    item = crud.item.create(db=db, obj_in=item_in)
    stored_item = crud.item.get(db=db, id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description


def test_update_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random.randint(0, 999)
    item_in = ItemCreate(title=title, description=description, price=price)
    item = crud.item.create(db=db, obj_in=item_in)
    description2 = random_lower_string()
    price2 = random.randint(0, 999)
    title2 = random_lower_string()
    item_update = ItemUpdate(description=description2, price=price2, title=title2)
    item2 = crud.item.update(db=db, db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item2.title == title2
    assert item2.description == description2
    assert item2.price == price2



def test_delete_item(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random.randint(0, 999)
    item_in = ItemCreate(title=title, description=description, price=price)
    user = create_random_user(db)
    item = crud.item.create(db=db, obj_in=item_in)
    item2 = crud.item.remove(db=db, id=item.id)
    item3 = crud.item.get(db=db, id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.title == title
    assert item2.description == description
