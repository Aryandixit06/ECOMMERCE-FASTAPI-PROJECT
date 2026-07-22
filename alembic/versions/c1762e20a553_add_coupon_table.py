"""add coupon table

Revision ID: c1762e20a553
Revises: 8f9c932838fb
Create Date: 2026-07-14 15:34:07.349462
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c1762e20a553"
down_revision: Union[str, Sequence[str], None] = "8f9c932838fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Use existing ENUM if already present
    discount_enum = postgresql.ENUM(
        "PERCENTAGE",
        "FIXED",
        name="discounttype",
        create_type=False,
    )

    op.create_table(
        "coupons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("discount_type", discount_enum, nullable=False),
        sa.Column("discount_value", sa.Float(), nullable=False),
        sa.Column("minimum_amount", sa.Float(), nullable=True),
        sa.Column("maximum_discount", sa.Float(), nullable=True),
        sa.Column("usage_limit", sa.Integer(), nullable=True),
        sa.Column("used_count", sa.Integer(), nullable=True),
        sa.Column("expiry_date", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_index(
        op.f("ix_coupons_code"),
        "coupons",
        ["code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_coupons_id"),
        "coupons",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f("ix_coupons_id"), table_name="coupons")
    op.drop_index(op.f("ix_coupons_code"), table_name="coupons")
    op.drop_table("coupons")