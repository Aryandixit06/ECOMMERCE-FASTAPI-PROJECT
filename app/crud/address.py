from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
)


def create_address(
    db: Session,
    user_id: int,
    address: AddressCreate,
):
    # Make first address default
    is_default = (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .count()
        == 0
    )

    db_address = Address(
        user_id=user_id,
        full_name=address.full_name,
        phone=address.phone,
        address_line=address.address_line,
        city=address.city,
        state=address.state,
        country=address.country,
        postal_code=address.postal_code,
        address_type=address.address_type,
        is_default=is_default,
    )

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


def get_user_addresses(
    db: Session,
    user_id: int,
):
    return (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .all()
    )


def update_address(
    db: Session,
    address_id: int,
    address: AddressUpdate,
):
    db_address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
    )

    if db_address is None:
        return None

    data = address.model_dump(exclude_unset=True)

    # If this address becomes default,
    # remove default from others
    if data.get("is_default"):
        db.query(Address).filter(
            Address.user_id == db_address.user_id
        ).update(
            {"is_default": False}
        )

    for key, value in data.items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)

    return db_address


def delete_address(
    db: Session,
    address_id: int,
):
    db_address = (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
    )

    if db_address is None:
        return None

    db.delete(db_address)
    db.commit()

    return db_address