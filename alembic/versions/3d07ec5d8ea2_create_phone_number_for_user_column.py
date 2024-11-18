"""create phone number for user column

Revision ID: 3d07ec5d8ea2
Revises: 
Create Date: 2024-07-29 13:22:03.439322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3d07ec5d8ea2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    pass
