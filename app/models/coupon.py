from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Enum as SqlEnum,
)

from app.core.database import Base


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    discount_type = Column(
        SqlEnum(DiscountType),
        nullable=False,
    )

    discount_value = Column(
        Float,
        nullable=False,
    )

    minimum_amount = Column(
        Float,
        default=0,
    )

    maximum_discount = Column(
        Float,
        nullable=True,
    )

    usage_limit = Column(
        Integer,
        default=1,
    )

    used_count = Column(
        Integer,
        default=0,
    )

    expiry_date = Column(
        DateTime,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )