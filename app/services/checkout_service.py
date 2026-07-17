from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.cart_repository import CartRepository
from app.repositories.checkout_repository import CheckoutRepository
from app.services.coupon_service import CouponService
from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)


class CheckoutService:

    @staticmethod
    def checkout(
        db: Session,
        current_user: User,
        request: CheckoutRequest,
    ):

        cart_items = CartRepository.get_cart_items(
            db,
            current_user.id,
        )

        if not cart_items:
            raise ValueError(
                "Cart is empty."
            )

        original_amount = 0

        for item in cart_items:

            if item.product.stock < item.quantity:
                raise ValueError(
                    f"{item.product.name} is out of stock."
                )

            original_amount += (
                item.product.price * item.quantity
            )

        discount = 0
        final_amount = original_amount

        try:
            if request.coupon_code:
                coupon_result = CouponService.apply_coupon(
                    db,
                    request.coupon_code,
                    original_amount,
                )

                discount = coupon_result.get("discount", 0)
                final_amount = coupon_result.get("final_amount", original_amount)

            order = CheckoutRepository.create_order(
                db,
                current_user.id,
                final_amount,
            )

            db.flush()

            for item in cart_items:

                CheckoutRepository.create_order_item(
                    db,
                    order.id,
                    item.product.id,
                    item.quantity,
                    item.product.price,
                )

                CheckoutRepository.reduce_stock(
                    item.product,
                    item.quantity,
                )

            CheckoutRepository.clear_cart(
                db,
                current_user.id,
            )

            db.commit()

            return CheckoutResponse(
                order_id=order.id,
                original_amount=original_amount,
                discount=discount,
                final_amount=final_amount,
                payment_status="Pending",
                message="Order created successfully.",
            )

        except Exception:

            db.rollback()

            raise