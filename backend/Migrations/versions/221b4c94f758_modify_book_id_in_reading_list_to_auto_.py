"""modify book_id in reading_list to auto increment

Revision ID: 221b4c94f758
Revises: dee77f2f80c0
Create Date: 2024-10-17 11:24:58.842605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '221b4c94f758'
down_revision: Union[str, None] = 'dee77f2f80c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS book_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Set the default of the column to use the sequence
    op.alter_column('reading_list', 'book_id', 
                    server_default=sa.text("nextval('book_id_seq')"))

    # Set the sequence to the max current value
    op.execute("SELECT setval('book_id_seq', (SELECT MAX(book_id) FROM reading_list));")
   


def downgrade() -> None:
    pass    # Drop the default if needed
    op.alter_column('reading_list', 'book_id', 
                    server_default=None)
    # Drop the sequence
    op.execute("DROP SEQUENCE book_id_seq;")
