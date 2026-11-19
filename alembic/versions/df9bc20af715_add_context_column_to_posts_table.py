"""add context column to posts table

Revision ID: df9bc20af715
Revises: 6ae83d912fe5
Create Date: 2025-08-07 10:49:39.684534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df9bc20af715'
down_revision: Union[str, Sequence[str], None] = '6ae83d912fe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
