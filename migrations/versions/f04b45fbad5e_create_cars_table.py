"""create cars table (superseded)

Revision ID: f04b45fbad5e
Revises: 0783f4c01ab1
Create Date: 2026-10-16 08:22:37.910018

Previously created an unused ``cars`` table that did not match the ``car``
model. Kept as a no-op so databases already stamped with this revision can
still be upgraded.
"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'f04b45fbad5e'
down_revision: Union[str, None] = '0783f4c01ab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
