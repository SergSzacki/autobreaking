"""create cars table

Revision ID: f04b45fbad5e
Revises: 0783f4c01ab1
Create Date: 2026-10-16 08:22:37.910018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f04b45fbad5e'
down_revision: Union[str, None] = '0783f4c01ab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cars',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('make', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=50), nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('cars')
