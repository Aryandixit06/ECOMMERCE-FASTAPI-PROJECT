from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    full_name = Column(
        String(100),
        nullable=False,
    )

    phone = Column(
        String(15),
        nullable=False,
    )

    address_line = Column(
        String(255),
        nullable=False,
    )

    city = Column(
        String(100),
        nullable=False,
    )

    state = Column(
        String(100),
        nullable=False,
    )

    country = Column(
        String(100),
        default="India",
    )

    postal_code = Column(
        String(10),
        nullable=False,
    )

    address_type = Column(
        String(20),
        default="Home",
    )

    is_default = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="addresses",
    )