from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.repositories.order_repository import OrderRepository


class OrderService:

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

        order = OrderRepository.create_order(
            db,
            order,
        )

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def add_order_item(
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

        order_item = OrderRepository.create_order_item(
            db,
            order_item,
        )

        db.commit()
        db.refresh(order_item)

        return order_item

    @staticmethod
    def get_orders(
        db: Session,
        user_id: int,
    ):
        return OrderRepository.get_orders(
            db,
            user_id,
        )

    @staticmethod
    def get_order(
        db: Session,
        order_id: int,
    ):
        return OrderRepository.get_order_by_id(
            db,
            order_id,
        )

    @staticmethod
    def update_status(
        db: Session,
        order_id: int,
        status: str,
    ):
        order = OrderRepository.get_order_by_id(
            db,
            order_id,
        )

        if order is None:
            return None

        order.status = status

        order = OrderRepository.update_order(
            db,
            order,
        )

        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def delete_order(
        db: Session,
        order_id: int,
    ):
        order = OrderRepository.get_order_by_id(
            db,
            order_id,
        )

        if order is None:
            return None

        OrderRepository.delete_order(
            db,
            order,
        )

        db.commit()

        return order