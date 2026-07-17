from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.order import OrderResponse
from app.crud.order import (
    create_order,
    get_my_orders,
    get_order_by_id,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=OrderResponse)
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = create_order(db, current_user.id)

    if order is None:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty",
        )

    return order


@router.get("/", response_model=list[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_orders(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_by_id(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order