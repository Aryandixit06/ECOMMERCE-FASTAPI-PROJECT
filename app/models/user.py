from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    is_admin = Column(Boolean, default=False)

    cart_items = relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete",
    )

    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete",
    )

    wishlist_items = relationship(
        "Wishlist",
        back_populates="user",
        cascade="all, delete",
    )

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete",
    )

    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete",
    )
    
    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete",
    )