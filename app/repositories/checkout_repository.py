from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository


class CheckoutRepository:

    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        total_price: float,
    ):
        order = Order(
            user_id=user_id,
            total_price=total_price,
            status="Pending",
        )

        OrderRepository.create_order(
            db,
            order,
        )

        return order

    @staticmethod
    def create_order_item(
        db: Session,
        order_id: int,
        product_id: int,
        quantity: int,
        price: float,
    ):
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )

        OrderRepository.create_order_item(
            db,
            order_item,
        )

        return order_item

    @staticmethod
    def reduce_stock(
        product: Product,
        quantity: int,
    ):
        product.stock -= quantity

    @staticmethod
    def clear_cart(
        db: Session,
        user_id: int,
    ):
        CartRepository.clear_cart(
            db,
            user_id,
        )