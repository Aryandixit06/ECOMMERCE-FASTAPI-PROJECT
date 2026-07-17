from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.models.user import User

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.schemas.pagination import PaginatedResponse
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService.create_product(db, product)


@router.get(
    "/",
    response_model=PaginatedResponse[ProductResponse],
)
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    search: str | None = Query(
        default=None,
        description="Search by product name or description",
    ),

    category_id: int | None = Query(
        default=None,
        description="Filter by category id",
    ),

    min_price: float | None = Query(
        default=None,
        description="Minimum product price",
    ),

    max_price: float | None = Query(
        default=None,
        description="Maximum product price",
    ),

    in_stock: bool | None = Query(
        default=None,
        description="Show only products in stock",
    ),

    sort_by: str = Query(
        default="id",
        description="Sort by: id, name, price, stock",
    ),

    order: str = Query(
        default="desc",
        description="Sort order: asc or desc",
    ),

    db: Session = Depends(get_db),
):
    return ProductService.get_products(
        db,
        page,
        limit,
        search,
        category_id,
        min_price,
        max_price,
        in_stock,
        sort_by,
        order,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = ProductService.get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_product = ProductService.update_product(
        db,
        product_id,
        product_update,
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return updated_product


@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_product = ProductService.delete_product(
        db,
        product_id,
    )

    if deleted_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return deleted_product
