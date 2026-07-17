from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.schemas.cart import CartCreate, CartUpdate


def add_to_cart(
    db: Session,
    user_id: int,
    cart: CartCreate,
):
    db_cart = CartItem(
        user_id=user_id,
        product_id=cart.product_id,
        quantity=cart.quantity,
    )

    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def get_user_cart(
    db: Session,
    user_id: int,
):
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )


def update_cart_item(
    db: Session,
    cart_id: int,
    cart: CartUpdate,
):
    db_cart = (
        db.query(CartItem)
        .filter(CartItem.id == cart_id)
        .first()
    )

    if db_cart is None:
        return None

    db_cart.quantity = cart.quantity

    db.commit()
    db.refresh(db_cart)

    return db_cart


def delete_cart_item(
    db: Session,
    cart_id: int,
):
    db_cart = (
        db.query(CartItem)
        .filter(CartItem.id == cart_id)
        .first()
    )

    if db_cart is None:
        return None

    db.delete(db_cart)
    db.commit()

    return db_cart