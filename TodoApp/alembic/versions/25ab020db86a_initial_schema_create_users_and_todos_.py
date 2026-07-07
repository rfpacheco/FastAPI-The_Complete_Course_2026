"""Initial schema: Create users and todos tables

Revision ID: 25ab020db86a
Revises:
Create Date: 2026-07-07 19:56:48.627700

This is the initial migration that establishes the baseline schema.
The users and todos tables already exist in the database.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25ab020db86a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    This is the baseline migration. The schema has already been initialized
    by docker/init.sql. Future migrations will track changes from this point.
    """
    pass


def downgrade() -> None:
    """Downgrade schema.

    Cannot downgrade the baseline migration.
    """
    pass
