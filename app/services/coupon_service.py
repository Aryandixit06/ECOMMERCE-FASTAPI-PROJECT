from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.coupon_repository import CouponRepository
from app.schemas.coupon import (
    CouponCreate,
    CouponUpdate,
)


class CouponService:

    @staticmethod
    def create_coupon(
        db: Session,
        coupon: CouponCreate,
    ):
        existing_coupon = CouponRepository.get_by_code(
            db,
            coupon.code,
        )

        if existing_coupon:
            raise ValueError(
                "Coupon code already exists."
            )

        db_coupon = CouponRepository.create(
            db,
            coupon,
        )

        db.commit()
        db.refresh(db_coupon)

        return db_coupon

    @staticmethod
    def get_coupons(
        db: Session,
    ):
        return CouponRepository.get_all(db)

    @staticmethod
    def get_coupon(
        db: Session,
        coupon_id: int,
    ):
        return CouponRepository.get_by_id(
            db,
            coupon_id,
        )

    @staticmethod
    def update_coupon(
        db: Session,
        coupon_id: int,
        coupon_update: CouponUpdate,
    ):
        coupon = CouponRepository.get_by_id(
            db,
            coupon_id,
        )

        if coupon is None:
            return None

        coupon = CouponRepository.update(
            db,
            coupon,
            coupon_update,
        )

        db.commit()
        db.refresh(coupon)

        return coupon

    @staticmethod
    def delete_coupon(
        db: Session,
        coupon_id: int,
    ):
        coupon = CouponRepository.get_by_id(
            db,
            coupon_id,
        )

        if coupon is None:
            return None

        CouponRepository.delete(
            db,
            coupon,
        )

        db.commit()

        return coupon

    @staticmethod
    def validate_coupon(
        db: Session,
        code: str,
        cart_total: float,
    ):
        coupon = CouponRepository.get_by_code(
            db,
            code,
        )

        if coupon is None:
            raise ValueError(
                "Coupon not found."
            )

        if not coupon.is_active:
            raise ValueError(
                "Coupon is inactive."
            )

        if coupon.expiry_date < datetime.utcnow():
            raise ValueError(
                "Coupon has expired."
            )

        if coupon.used_count >= coupon.usage_limit:
            raise ValueError(
                "Coupon usage limit exceeded."
            )

        if cart_total < coupon.minimum_amount:
            raise ValueError(
                f"Minimum order amount should be ₹{coupon.minimum_amount}"
            )

        return coupon

    @staticmethod
    def apply_coupon(
        db: Session,
        code: str,
        cart_total: float,
    ):
        coupon = CouponService.validate_coupon(
            db,
            code,
            cart_total,
        )

        if coupon.discount_type.value == "fixed":
            discount = coupon.discount_value

        else:
            discount = (
                cart_total * coupon.discount_value
            ) / 100

            if (
                coupon.maximum_discount is not None
                and discount > coupon.maximum_discount
            ):
                discount = coupon.maximum_discount

        final_amount = cart_total - discount

        if final_amount < 0:
            final_amount = 0

        coupon.used_count += 1

        return {
            "coupon_code": coupon.code,
            "original_amount": cart_total,
            "discount": discount,
            "final_amount": final_amount,
        }