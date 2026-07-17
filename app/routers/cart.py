from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.cart import (
    CartCreate,
    CartUpdate,
    CartResponse,
)

from app.crud.cart import (
    add_to_cart,
    get_user_cart,
    update_cart_item,
    delete_cart_item,
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("/", response_model=CartResponse)
def add_cart_item(
    cart: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_to_cart(db, current_user.id, cart)


@router.get("/", response_model=list[CartResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_cart(db, current_user.id)


@router.put("/{cart_id}", response_model=CartResponse)
def update_cart(
    cart_id: int,
    cart: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = update_cart_item(db, cart_id, cart)

    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return cart_item


@router.delete("/{cart_id}", response_model=CartResponse)
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = delete_cart_item(db, cart_id)

    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return cart_item