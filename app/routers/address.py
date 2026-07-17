from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)

from app.crud.address import (
    create_address,
    get_user_addresses,
    update_address,
    delete_address,
)

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


@router.post("/", response_model=AddressResponse)
def add_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_address(
        db,
        current_user.id,
        address,
    )


@router.get("/", response_model=list[AddressResponse])
def my_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_addresses(
        db,
        current_user.id,
    )


@router.put("/{address_id}", response_model=AddressResponse)
def edit_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_address(
        db,
        address_id,
        address,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    return updated


@router.delete("/{address_id}", response_model=AddressResponse)
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_address(
        db,
        address_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    return deleted