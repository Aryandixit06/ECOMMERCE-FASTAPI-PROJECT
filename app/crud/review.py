from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from sqlalchemy import func
from app.models.product import Product


def create_review(
    db: Session,
    user_id: int,
    review: ReviewCreate,
):
    # Prevent duplicate review
    existing_review = (
        db.query(Review)
        .filter(
            Review.user_id == user_id,
            Review.product_id == review.product_id,
        )
        .first()
    )

    if existing_review:
        return None

    db_review = Review(
        user_id=user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def get_product_reviews(
    db: Session,
    product_id: int,
):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .all()
    )


def update_review(
    db: Session,
    review_id: int,
    review: ReviewUpdate,
):
    db_review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )

    if db_review is None:
        return None

    if review.rating is not None:
        db_review.rating = review.rating

    if review.comment is not None:
        db_review.comment = review.comment

    db.commit()
    db.refresh(db_review)

    return db_review


def delete_review(
    db: Session,
    review_id: int,
):
    db_review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )

    if db_review is None:
        return None

    db.delete(db_review)
    db.commit()

    return db_review

def get_product_rating(db: Session, product_id: int):
    average_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.product_id == product_id)
        .scalar()
    )

    total_reviews = (
        db.query(func.count(Review.id))
        .filter(Review.product_id == product_id)
        .scalar()
    )

    return {
        "product_id": product_id,
        "average_rating": round(average_rating or 0, 2),
        "total_reviews": total_reviews,
    }
    
def top_rated_products(db: Session):
    return (
        db.query(
            Product.id,
            Product.name,
            func.avg(Review.rating).label("average_rating"),
            func.count(Review.id).label("total_reviews"),
        )
        .join(Review, Product.id == Review.product_id)
        .group_by(Product.id, Product.name)
        .order_by(func.avg(Review.rating).desc())
        .all()
    )