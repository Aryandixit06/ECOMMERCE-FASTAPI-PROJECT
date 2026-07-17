from sqlalchemy.orm import Session

from app.models.coupon import Coupon
from app.schemas.coupon import (
    CouponCreate,
    CouponUpdate,
)


class CouponRepository:

    @staticmethod
    def create(
        db: Session,
        coupon: CouponCreate,
    ):
        db_coupon = Coupon(
            code=coupon.code,
            discount_type=coupon.discount_type,
            discount_value=coupon.discount_value,
            minimum_amount=coupon.minimum_amount,
            maximum_discount=coupon.maximum_discount,
            usage_limit=coupon.usage_limit,
            expiry_date=coupon.expiry_date,
            is_active=coupon.is_active,
        )

        db.add(db_coupon)
        db.commit()
        db.refresh(db_coupon)

        return db_coupon

    @staticmethod
    def get_all(db: Session):
        return db.query(Coupon).all()

    @staticmethod
    def get_by_id(
        db: Session,
        coupon_id: int,
    ):
        return (
            db.query(Coupon)
            .filter(Coupon.id == coupon_id)
            .first()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        code: str,
    ):
        return (
            db.query(Coupon)
            .filter(Coupon.code == code)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        coupon: Coupon,
        coupon_update: CouponUpdate,
    ):
        update_data = coupon_update.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(coupon, key, value)

        db.commit()
        db.refresh(coupon)

        return coupon

    @staticmethod
    def delete(
        db: Session,
        coupon: Coupon,
    ):
        db.delete(coupon)
        db.commit()