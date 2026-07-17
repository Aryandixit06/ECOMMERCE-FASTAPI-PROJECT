from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class CouponBase(BaseModel):
    code: str = Field(..., max_length=50)

    discount_type: DiscountType

    discount_value: float = Field(..., gt=0)

    minimum_amount: float = Field(
        default=0,
        ge=0,
    )

    maximum_discount: float | None = Field(
        default=None,
        ge=0,
    )

    usage_limit: int = Field(
        default=1,
        ge=1,
    )

    expiry_date: datetime

    is_active: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    code: str | None = None

    discount_type: DiscountType | None = None

    discount_value: float | None = Field(
        default=None,
        gt=0,
    )

    minimum_amount: float | None = Field(
        default=None,
        ge=0,
    )

    maximum_discount: float | None = Field(
        default=None,
        ge=0,
    )

    usage_limit: int | None = Field(
        default=None,
        ge=1,
    )

    expiry_date: datetime | None = None

    is_active: bool | None = None


class CouponResponse(CouponBase):
    id: int
    used_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ApplyCouponRequest(BaseModel):
    code: str
    cart_total: float


class ApplyCouponResponse(BaseModel):
    coupon_code: str
    original_amount: float
    discount: float
    final_amount: float