from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentVerify,
    VerifyPaymentResponse,
    CreatePaymentResponse,
)

from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/create-order",
    response_model=CreatePaymentResponse,
)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return PaymentService.create_payment(
            db,
            current_user,
            payment_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/verify",
    response_model=VerifyPaymentResponse,
)
def verify_payment(
    payment_data: PaymentVerify,
    db: Session = Depends(get_db),
):
    try:
        return PaymentService.verify_payment(
            db,
            payment_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = PaymentService.get_payment(
        db,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found.",
        )

    return payment


@router.get(
    "/history",
    response_model=list[PaymentResponse],
)
def payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PaymentService.get_payment_history(
        db,
        current_user.id,
    )