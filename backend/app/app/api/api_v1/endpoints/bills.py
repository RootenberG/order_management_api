from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Bill])
def read_bills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bills.
    """
    if not (crud.user.is_superuser(current_user) or crud.user.is_cashier(current_user)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    items = crud.bill.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/my", response_model=List[schemas.Bill])
def read_user_bills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bills of current user.
    """
    if not (
        crud.user.is_superuser(current_user) or not crud.user.is_staff(current_user)
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    items = crud.bill.get_multi_by_user(db, user=current_user, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Bill)
def create_bill(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.BillCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bill.
    """
    if not (crud.user.is_superuser(current_user) or crud.user.is_cashier(current_user)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bill = crud.bill.create(db=db, obj_in=item_in)
    return bill


@router.put(
    "/{id}",
    response_model=schemas.Bill,
    response_model_include={"id", "status", "bill_created_date"},
)
def update_bill(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.BillUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a bill.
    """
    bill = crud.bill.get(db=db, id=id)
    if not bill:
        raise HTTPException(status_code=404, detail="Item not found")
    if not (crud.user.is_superuser(current_user) or crud.user.is_cashier(current_user)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.update(db=db, db_obj=bill, obj_in=item_in)
    return item
