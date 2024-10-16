"""Modify password column to more than 100 characters

Revision ID: a11b28bd6c93
Revises: 
Create Date: 2024-10-16 12:56:29.570236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a11b28bd6c93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Change the column type from VARCHAR(100) to VARCHAR(255)
    op.alter_column('users', 'password',
                    type_=sa.String(length=255),
                    existing_type=sa.String(length=100))


def downgrade() -> None:
    # Revert the change: change the column type back to VARCHAR(100)
    op.alter_column('users', 'password',
                    type_=sa.String(length=100),
                    existing_type=sa.String(length=255))
