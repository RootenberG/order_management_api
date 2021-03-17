from typing import Any, List, Optional
from datetime import date

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    if crud.user.is_staff(current_user) or crud.user.is_superuser(current_user):
        orders = crud.order.get_multi(
            db, skip=skip, limit=limit, start_date=start_date, end_date=end_date
        )
        return orders
    else:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges",
        )


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user.
    """
    if crud.order.in_progres(db, obj_in=current_user):
        raise HTTPException(
            status_code=400,
            detail="You already have an order in progres.",
        )
    order = crud.order.create(db, obj_in=order_in)
    return order


@router.put("/{id}", response_model=schemas.Order)
def update_order_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update order status.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if crud.user.is_cashier(current_user):
        if item_in.status == "approved_by_cashier":
            if order.status != "in_progres":
                raise HTTPException(status_code=400, detail="Order must be in progres")
            else:
                order = crud.order.update(db, db_obj=order, obj_in=item_in)
        elif item_in.status == "paid":
            if order.status != "done":
                raise HTTPException(status_code=400, detail="Order must be done")
            bill = crud.bill.get_by_order(db, order=order)
            if not bill:
                raise HTTPException(status_code=404, detail="Bill not found")
            if bill.status != "paid":
                raise HTTPException(status_code=400, detail="Bill must be paid")
            order = crud.order.update(db, db_obj=order, obj_in=item_in)

        else:
            raise HTTPException(status_code=400, detail="Invalid status")
    elif crud.user.is_seller(current_user):
        if item_in.status == "done":
            if order.status != "approved_by_cashier":
                raise HTTPException(
                    status_code=400, detail="Order must be approved by cashier"
                )
            else:
                order = crud.order.update(db, db_obj=order, obj_in=item_in)
        else:
            raise HTTPException(status_code=400, detail="Invalid status")
    elif crud.user.is_superuser(current_user):
        order = crud.order.update(db, db_obj=order, obj_in=item_in)
    else:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return order


# @router.get("/me", response_model=schemas.User)
# def read_user_me(
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get current user.
#     """
#     return current_user


# @router.post("/open", response_model=schemas.User)
# def create_user_open(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(...),
#     email: EmailStr = Body(...),
#     full_name: str = Body(None),
# ) -> Any:
#     """
#     Create new user without the need to be logged in.
#     """
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open user registration is forbidden on this server",
#         )
#     user = crud.user.get_by_email(db, email=email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system",
#         )
#     user_in = schemas.it(password=password, email=email, full_name=full_name)
#     user = crud.user.create(db, obj_in=user_in)
#     return user


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user_by_id(
#     user_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Get a specific user by id.
#     """
#     user = crud.user.get(db, id=user_id)
#     if user == current_user:
#         return user
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user


# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user
