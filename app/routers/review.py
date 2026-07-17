from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
)

from app.crud.review import (
    create_review,
    get_product_reviews,
    update_review,
    delete_review,
    get_product_rating,
    top_rated_products,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post("/", response_model=ReviewResponse)
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_review = create_review(
        db,
        current_user.id,
        review,
    )

    if db_review is None:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product.",
        )

    return db_review


@router.get("/product/{product_id}", response_model=list[ReviewResponse])
def product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_product_reviews(
        db,
        product_id,
    )


@router.put("/{review_id}", response_model=ReviewResponse)
def edit_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_review(
        db,
        review_id,
        review,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return updated


@router.delete("/{review_id}", response_model=ReviewResponse)
def remove_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_review(
        db,
        review_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return deleted

@router.get("/product/{product_id}/rating")
def product_rating(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_product_rating(db, product_id)


@router.get("/top-rated")
def get_top_rated_products(
    db: Session = Depends(get_db),
):
    return top_rated_products(db)