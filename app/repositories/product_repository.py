from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:

    @staticmethod
    def create(
        db: Session,
        product: ProductCreate,
    ):
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            is_active=product.is_active,
            category_id=product.category_id,
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    @staticmethod
    def get_all(
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
        query = db.query(Product)

        # -----------------------
        # Search Filter
        # -----------------------
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        # -----------------------
        # Category Filter
        # -----------------------
        if category_id is not None:
            query = query.filter(
                Product.category_id == category_id
            )

        # -----------------------
        # Minimum Price Filter
        # -----------------------
        if min_price is not None:
            query = query.filter(
                Product.price >= min_price
            )

        # -----------------------
        # Maximum Price Filter
        # -----------------------
        if max_price is not None:
            query = query.filter(
                Product.price <= max_price
            )

        # -----------------------
        # Stock Filter
        # -----------------------
        if in_stock:
            query = query.filter(
                Product.stock > 0
            )

        # -----------------------
        # Sorting
        # -----------------------
        if hasattr(Product, sort_by):
            column = getattr(Product, sort_by)

            if order.lower() == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())

        # -----------------------
        # Pagination
        # -----------------------
        skip = (page - 1) * limit

        # Total Records
        total = query.count()

        # Current Page Records
        products = (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            "items": products,
            "total": total,
        }

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int,
    ):
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
        product_update: ProductUpdate,
    ):
        update_data = product_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(
        db: Session,
        product: Product,
    ):
        db.delete(product)
        db.commit()