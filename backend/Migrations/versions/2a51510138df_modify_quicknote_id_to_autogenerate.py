"""modify quicknote id to autogenerate

Revision ID: 2a51510138df
Revises: f7a925ca459c
Create Date: 2024-10-18 10:37:49.290717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a51510138df'
down_revision: Union[str, None] = 'f7a925ca459c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS quick_notes_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Set the default of the column to use the sequence
    op.alter_column('quick_notes', 'quick_notes_id', 
                    server_default=sa.text("nextval('quick_notes_id_seq')"))

    # Set the sequence to the max current value
    op.execute("SELECT setval('quick_notes_id_seq', (SELECT MAX(quick_notes_id) FROM quick_notes);")



def downgrade() -> None:
    # Drop the default if needed
    op.alter_column('quick_notes', 'quick_notes_id', 
                    server_default=None)
    # Drop the sequence
    op.execute("DROP SEQUENCE quick_notes_id_seq;")

