"""Modify movie id to autogenerate

Revision ID: f7a925ca459c
Revises: 221b4c94f758
Create Date: 2024-10-17 20:06:03.849758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7a925ca459c'
down_revision: Union[str, None] = '221b4c94f758'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS movie_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Set the default of the column to use the sequence
    op.alter_column('movie_list', 'movie_id', 
                    server_default=sa.text("nextval('movie_id_seq')"))

    # Set the sequence to the max current value
    op.execute("SELECT setval('movie_id_seq', (SELECT MAX(movie_id) FROM movie_list));")


def downgrade() -> None:
    # Drop the default if needed
    op.alter_column('movie_list', 'movie_id', 
                    server_default=None)
    # Drop the sequence
    op.execute("DROP SEQUENCE movie_id_seq;")
