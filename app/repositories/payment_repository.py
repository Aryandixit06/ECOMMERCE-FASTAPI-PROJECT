from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def create(
        db: Session,
        payment: Payment,
    ):
        db.add(payment)
        return payment

    @staticmethod
    def get_by_id(
        db: Session,
        payment_id: int,
    ):
        return (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    @staticmethod
    def get_by_order_id(
        db: Session,
        order_id: int,
    ):
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

    @staticmethod
    def get_by_razorpay_order_id(
        db: Session,
        razorpay_order_id: str,
    ):
        return (
            db.query(Payment)
            .filter(
                Payment.razorpay_order_id == razorpay_order_id
            )
            .first()
        )

    @staticmethod
    def get_user_payments(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Payment)
            .filter(Payment.user_id == user_id)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        payment: Payment,
    ):
        return payment

    @staticmethod
    def delete(
        db: Session,
        payment: Payment,
    ):
        db.delete(payment)