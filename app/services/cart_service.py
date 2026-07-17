from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.repositories.cart_repository import CartRepository


class CartService:

    @staticmethod
    def get_cart(
        db: Session,
        user_id: int,
    ):
        return CartRepository.get_cart_items(
            db,
            user_id,
        )

    @staticmethod
    def add_to_cart(
        db: Session,
        user_id: int,
        product_id: int,
        quantity: int,
    ):
        cart_item = CartRepository.get_cart_item(
            db,
            user_id,
            product_id,
        )

        if cart_item:
            cart_item.quantity += quantity

            cart_item = CartRepository.update(
                db,
                cart_item,
            )

            db.commit()
            db.refresh(cart_item)

            return cart_item

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )

        cart_item = CartRepository.create(
            db,
            cart_item,
        )

        db.commit()
        db.refresh(cart_item)

        return cart_item

    @staticmethod
    def remove_from_cart(
        db: Session,
        user_id: int,
        product_id: int,
    ):
        cart_item = CartRepository.get_cart_item(
            db,
            user_id,
            product_id,
        )

        if cart_item is None:
            return None

        CartRepository.delete(
            db,
            cart_item,
        )

        db.commit()

        return cart_item

    @staticmethod
    def clear_cart(
        db: Session,
        user_id: int,
    ):
        CartRepository.clear_cart(
            db,
            user_id,
        )

        db.commit()