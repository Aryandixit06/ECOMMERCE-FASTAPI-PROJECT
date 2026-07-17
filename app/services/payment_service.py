import razorpay

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.payment import Payment
from app.models.user import User

from app.repositories.payment_repository import (
    PaymentRepository,
)
from app.repositories.order_repository import (
    OrderRepository,
)

from app.schemas.payment import (
    PaymentCreate,
    PaymentVerify,
    VerifyPaymentResponse,
)


class PaymentService:

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    @staticmethod
    def create_payment(
        db: Session,
        current_user: User,
        payment_data: PaymentCreate,
    ):

        order = OrderRepository.get_order_by_id(
            db,
            payment_data.order_id,
        )

        if order is None:
            raise ValueError(
                "Order not found."
            )

        if order.user_id != current_user.id:
            raise ValueError(
                "You are not allowed to pay for this order."
            )

        existing_payment = (
            PaymentRepository.get_by_order_id(
                db,
                order.id,
            )
        )

        if existing_payment:
            raise ValueError(
                "Payment already exists for this order."
            )

        amount = int(order.total_price * 100)

        razorpay_order = (
            PaymentService.client.order.create(
                {
                    "amount": amount,
                    "currency": "INR",
                    "payment_capture": 1,
                }
            )
        )

        payment = Payment(
            order_id=order.id,
            user_id=current_user.id,
            razorpay_order_id=razorpay_order["id"],
            amount=order.total_price,
            currency=razorpay_order["currency"],
            status="Pending",
        )

        payment = PaymentRepository.create(
            db,
            payment,
        )

        db.commit()
        db.refresh(payment)

        return {
            "payment_id": payment.id,
            "razorpay_order_id": razorpay_order["id"],
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
        }
        
        from app.schemas.payment import (
    PaymentVerify,
    VerifyPaymentResponse,
)


    @staticmethod
    def verify_payment(
        db: Session,
        payment_data: PaymentVerify,
    ):

        payment = PaymentRepository.get_by_razorpay_order_id(
            db,
            payment_data.razorpay_order_id,
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        try:

            PaymentService.client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": payment_data.razorpay_order_id,
                    "razorpay_payment_id": payment_data.razorpay_payment_id,
                    "razorpay_signature": payment_data.razorpay_signature,
                }
            )

            payment.razorpay_payment_id = (
                payment_data.razorpay_payment_id
            )

            payment.razorpay_signature = (
                payment_data.razorpay_signature
            )

            payment.status = "Success"

            PaymentRepository.update(
                db,
                payment,
            )

            order = OrderRepository.get_order_by_id(
                db,
                payment.order_id,
            )

            order.status = "Paid"

            OrderRepository.update_order(
                db,
                order,
            )

            db.commit()

            return VerifyPaymentResponse(
                message="Payment Verified Successfully",
                status="Success",
            )

        except Exception:

            db.rollback()

            payment.status = "Failed"

            db.commit()

            raise ValueError(
                "Payment Verification Failed."
            )