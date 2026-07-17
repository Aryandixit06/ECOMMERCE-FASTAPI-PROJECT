from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.admin import get_current_admin
from app.models.user import User
from fastapi import APIRouter

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

from app.crud.category import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/", response_model=CategoryResponse)
def create_category_endpoint(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return create_category(db, category)


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
):
    return get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = get_category_by_id(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    updated_category = update_category(
        db,
        category_id,
        category,
    )

    if updated_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return updated_category


@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    deleted_category = delete_category(db, category_id)

    if deleted_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return deleted_category

