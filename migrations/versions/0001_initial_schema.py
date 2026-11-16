"""initial car table

Revision ID: 0001_initial
Revises: f04b45fbad5e
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = 'f04b45fbad5e'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table("car"):
        return
    op.create_table(
        "car",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("make", sa.String(length=255), nullable=False),
        sa.Column("model", sa.String(length=255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("vin", sa.String(length=255), nullable=True),
        sa.Column("mileage", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("color", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True, server_default="available"),
    )


def downgrade():
    op.drop_table("car")
