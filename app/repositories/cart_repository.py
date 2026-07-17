from sqlalchemy.orm import Session

from app.models.cart import CartItem


class CartRepository:

    @staticmethod
    def get_cart_items(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_cart_item(
        db: Session,
        user_id: int,
        product_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        cart_item: CartItem,
    ):
        db.add(cart_item)
        return cart_item

    @staticmethod
    def update(
        db: Session,
        cart_item: CartItem,
    ):
        return cart_item

    @staticmethod
    def delete(
        db: Session,
        cart_item: CartItem,
    ):
        db.delete(cart_item)

    @staticmethod
    def clear_cart(
        db: Session,
        user_id: int,
    ):
        (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id)
            .delete()
        )