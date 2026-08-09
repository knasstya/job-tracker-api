"""add unique constraint to user email

Revision ID: 0e7c5e1a7342
Revises: aeca19176119
Create Date: 2026-08-09 15:10:29.948448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e7c5e1a7342'
down_revision: Union[str, Sequence[str], None] = 'aeca19176119'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique"
    )


