from sqlalchemy.orm import Session

from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate


def add_to_wishlist(
    db: Session,
    user_id: int,
    wishlist: WishlistCreate,
):
    # Prevent duplicate wishlist items
    existing_item = (
        db.query(Wishlist)
        .filter(
            Wishlist.user_id == user_id,
            Wishlist.product_id == wishlist.product_id,
        )
        .first()
    )

    if existing_item:
        return existing_item

    db_wishlist = Wishlist(
        user_id=user_id,
        product_id=wishlist.product_id,
    )

    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)

    return db_wishlist


def get_user_wishlist(
    db: Session,
    user_id: int,
):
    return (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id)
        .all()
    )


def remove_from_wishlist(
    db: Session,
    wishlist_id: int,
):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.id == wishlist_id)
        .first()
    )

    if wishlist_item is None:
        return None

    db.delete(wishlist_item)
    db.commit()

    return wishlist_item