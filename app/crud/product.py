from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate):
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


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product =  db.query(Product).filter(Product.id == product_id).first()
    
    if db_product is None:
        return None
    
    if product_update.name is not None:
        db_product.name = product_update.name
        if product_update.description is not None:
            db_product.description = product_update.description
            if product_update.price is not None:
                db_product.price = product_update.price
                if product_update.stock is not None:
                    db_product.stock = product_update.stock
                    if product_update.is_active is not None:
                        db_product.is_active = product_update.is_active       

                        db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if db_product is None:
        return None
    
    db.delete(db_product)
    db.commit()
    
    return db_product

