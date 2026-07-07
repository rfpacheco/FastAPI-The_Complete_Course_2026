"""Make phone_number NOT NULL for users

Revision ID: 5200bf7713bd
Revises: 25ab020db86a
Create Date: 2026-07-07 20:40:51.256832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5200bf7713bd'
down_revision: Union[str, Sequence[str], None] = '25ab020db86a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    1. Set any NULL phone_numbers to empty string (data migration)
    2. Add NOT NULL constraint
    """
    # First: Update any NULL phone_number values to empty string
    op.execute("UPDATE users SET phone_number = '' WHERE phone_number IS NULL")

    # Then: Apply NOT NULL constraint
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema.

    Revert the NOT NULL constraint, allowing NULL values again.
    """
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
