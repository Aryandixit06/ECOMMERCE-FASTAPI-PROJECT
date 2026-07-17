from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    razorpay_order_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    razorpay_payment_id = Column(
        String,
        nullable=True,
    )

    razorpay_signature = Column(
        String,
        nullable=True,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    currency = Column(
        String,
        default="INR",
    )

    status = Column(
        String,
        default="Pending",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    order = relationship(
        "Order",
        back_populates="payment",
    )

    user = relationship(
        "User",
        back_populates="payments",
    )