from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)

from app.services.checkout_service import CheckoutService

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
)


@router.post(
    "/",
    response_model=CheckoutResponse,
)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return CheckoutService.checkout(
            db,
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )