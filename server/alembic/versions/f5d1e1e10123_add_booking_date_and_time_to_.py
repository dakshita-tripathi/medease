"""add booking date and time to appointments

Revision ID: f5d1e1e10123
Revises: 593c6f2098e6
Create Date: 2025-12-27 16:15:15.584533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d1e1e10123'
down_revision: Union[str, Sequence[str], None] = '593c6f2098e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "appointments",
        sa.Column("booking_date", sa.Date(), nullable=True),
    )
    op.add_column(
        "appointments",
        sa.Column("booking_time", sa.Time(), nullable=True),
    )

    # 2. Backfill existing rows
    op.execute(
        """
        UPDATE appointments
        SET booking_date = '1970-01-01',
            booking_time = '00:00:00'
        """
    )

    # 3. Alter columns to NOT NULL
    op.alter_column("appointments", "booking_date", nullable=False)
    op.alter_column("appointments", "booking_time", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("appointments", "booking_time")
    op.drop_column("appointments", "booking_date")
