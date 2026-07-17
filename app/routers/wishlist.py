from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.wishlist import (
    WishlistCreate,
    WishlistResponse,
)

from app.crud.wishlist import (
    add_to_wishlist,
    get_user_wishlist,
    remove_from_wishlist,
)

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"],
)


@router.post("/", response_model=WishlistResponse)
def add_product_to_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_to_wishlist(
        db,
        current_user.id,
        wishlist,
    )


@router.get("/", response_model=list[WishlistResponse])
def my_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_wishlist(
        db,
        current_user.id,
    )


@router.delete("/{wishlist_id}", response_model=WishlistResponse)
def delete_wishlist_item(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wishlist = remove_from_wishlist(
        db,
        wishlist_id,
    )

    if wishlist is None:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found",
        )

    return wishlist