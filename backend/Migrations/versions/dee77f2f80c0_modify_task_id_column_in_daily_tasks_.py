"""modify task_id column in daily_tasks_list to auto increment

Revision ID: dee77f2f80c0
Revises: f0355b5714b3
Create Date: 2024-10-16 17:43:23.103889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dee77f2f80c0'
down_revision: Union[str, None] = 'f0355b5714b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Create the sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS task_id_seq START WITH 1 INCREMENT BY 1;")
    
    # Set the default of the column to use the sequence
    op.alter_column('daily_tasks_list', 'task_id', 
                    server_default=sa.text("nextval('task_id_seq')"))

    # Set the sequence to the max current value
    op.execute("SELECT setval('task_id_seq', (SELECT MAX(task_id) FROM daily_tasks_list));")


def downgrade() -> None:
    # Drop the default if needed
    op.alter_column('daily_tasks_list', 'task_id', 
                    server_default=None)
    # Drop the sequence
    op.execute("DROP SEQUENCE task_id_seq;")
