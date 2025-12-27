"""add username to users

Revision ID: 593c6f2098e6
Revises: 57a9d0f691ec
Create Date: 2025-12-26 20:48:33.963569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '593c6f2098e6'
down_revision: Union[str, Sequence[str], None] = '57a9d0f691ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column("username", sa.String(length=255), nullable=True)
    )

    # 2️⃣ Populate existing rows
    op.execute(
        "UPDATE users SET username = email WHERE username IS NULL"
    )

    # 3️⃣ Make column NOT NULL
    op.alter_column(
        "users",
        "username",
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "username")
