from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        order: Order,
    ):
        db.add(order)
        return order

    @staticmethod
    def create_order_item(
        db: Session,
        order_item: OrderItem,
    ):
        db.add(order_item)
        return order_item

    @staticmethod
    def get_orders(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_order_by_id(
        db: Session,
        order_id: int,
    ):
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def update_order(
        db: Session,
        order: Order,
    ):
        return order

    @staticmethod
    def delete_order(
        db: Session,
        order: Order,
    ):
        db.delete(order)