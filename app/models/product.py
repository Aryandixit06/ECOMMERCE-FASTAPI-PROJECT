from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)

    description = Column(String, index=True)

    price = Column(Float, index=True)

    stock = Column(Integer, index=True)

    is_active = Column(Boolean, default=True)

    image_url = Column(String, nullable=True)

    brand = Column(String, nullable=True)

    rating = Column(Float, default=0.0)

    discount_percentage = Column(Integer, default=0)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete",
    )

    wishlist_items = relationship(
        "Wishlist",
        back_populates="product",
        cascade="all, delete",
    )

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete",
    )