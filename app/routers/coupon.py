from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.coupon import (
    CouponCreate,
    CouponUpdate,
    CouponResponse,
    ApplyCouponRequest,
    ApplyCouponResponse,
)

from app.services.coupon_service import CouponService


router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"],
)


@router.post("/", response_model=CouponResponse)
def create_coupon(
    coupon: CouponCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return CouponService.create_coupon(
            db,
            coupon,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[CouponResponse])
def get_all_coupons(
    db: Session = Depends(get_db),
):
    return CouponService.get_coupons(db)


@router.get("/{coupon_id}", response_model=CouponResponse)
def get_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
):
    coupon = CouponService.get_coupon(
        db,
        coupon_id,
    )

    if coupon is None:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found",
        )

    return coupon


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    coupon_update: CouponUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    coupon = CouponService.update_coupon(
        db,
        coupon_id,
        coupon_update,
    )

    if coupon is None:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found",
        )

    return coupon


@router.delete("/{coupon_id}", response_model=CouponResponse)
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    coupon = CouponService.delete_coupon(
        db,
        coupon_id,
    )

    if coupon is None:
        raise HTTPException(
            status_code=404,
            detail="Coupon not found",
        )

    return coupon


@router.post(
    "/apply",
    response_model=ApplyCouponResponse,
)
def apply_coupon(
    request: ApplyCouponRequest,
    db: Session = Depends(get_db),
):
    try:
        return CouponService.apply_coupon(
            db,
            request.code,
            request.cart_total,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )