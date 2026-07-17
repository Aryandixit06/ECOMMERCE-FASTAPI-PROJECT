from math import ceil
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        product: ProductCreate,
    ):
        db_product = ProductRepository.create(
            db,
            product,
        )

        db.commit()
        db.refresh(db_product)

        return db_product

    @staticmethod
    def get_products(
        db: Session,
        page: int,
        limit: int,
        search: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool | None = None,
        sort_by: str = "id",
        order: str = "desc",
    ):
        result = ProductRepository.get_all(
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

        total = result["total"]
        items = result["items"]

        total_pages = ceil(total / limit) if total > 0 else 1

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "items": items,
        }

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ):
        return ProductRepository.get_by_id(
            db,
            product_id,
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_update: ProductUpdate,
    ):
        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            return None

        product = ProductRepository.update(
            db,
            product,
            product_update,
        )

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ):
        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            return None

        ProductRepository.delete(
            db,
            product,
        )

        db.commit()

        return product
    
