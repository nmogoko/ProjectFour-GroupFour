"""modify id column in user table to auto-generate

Revision ID: f0355b5714b3
Revises: a11b28bd6c93
Create Date: 2024-10-16 13:25:57.976490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0355b5714b3'
down_revision: Union[str, None] = 'a11b28bd6c93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   # Create the sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS user_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Set the default of the column to use the sequence
    op.alter_column('users', 'id', 
                    server_default=sa.text("nextval('user_id_seq')"))

    # Set the sequence to the max current value
    op.execute("SELECT setval('user_id_seq', (SELECT MAX(id) FROM users));")

def downgrade() -> None:
    # Drop the default if needed
    op.alter_column('users', 'id', 
                    server_default=None)
    # Drop the sequence
    op.execute("DROP SEQUENCE user_id_seq;")
