"""align car/part schema with the models

Creates the ``part`` table if it is missing and adds any missing columns
(min_quantity, supplier, location, notes, description, photos, timestamps)
to tables that were previously created by ``SQLModel.metadata.create_all``.

Revision ID: 0002_car_part_schema
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '0002_car_part_schema'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

PHOTOS_TYPE = sa.JSON().with_variant(JSONB(), "postgresql")


def _timestamp_columns():
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    ]


def _car_columns():
    return [
        sa.Column("color", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="available"),
        *_timestamp_columns(),
    ]


def _part_columns():
    return [
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("sku", sa.String(length=100), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min_quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("price", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("supplier", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("photos", PHOTOS_TYPE, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("car_id", sa.Integer(), sa.ForeignKey("car.id", ondelete="SET NULL"), nullable=True),
        *_timestamp_columns(),
    ]


def _add_missing_columns(inspector, table, columns):
    existing = {column["name"] for column in inspector.get_columns(table)}
    missing = [column for column in columns if column.name not in existing and column.name != "car_id"]
    if not missing:
        return
    # SQLite cannot ADD COLUMN with a non-constant default (CURRENT_TIMESTAMP), so rebuild the table there.
    recreate = "always" if op.get_bind().dialect.name == "sqlite" else "auto"
    with op.batch_alter_table(table, recreate=recreate) as batch:
        for column in missing:
            batch.add_column(column)


def _create_index_if_missing(inspector, name, table, columns, **kwargs):
    if name not in {index["name"] for index in inspector.get_indexes(table)}:
        op.create_index(name, table, columns, **kwargs)


def _normalize_legacy_part(bind, inspector):
    op.execute("UPDATE part SET price = 0 WHERE price IS NULL")
    with op.batch_alter_table("part") as batch:
        batch.alter_column("price", type_=sa.Numeric(12, 2), nullable=False, server_default="0")
        batch.alter_column("description", type_=sa.Text())
        batch.alter_column("notes", type_=sa.Text())

    photos = next(c for c in sa.inspect(bind).get_columns("part") if c["name"] == "photos")
    if photos["nullable"] or not isinstance(photos["type"], (sa.JSON, JSONB)):
        op.execute("UPDATE part SET photos = '[]' WHERE photos IS NULL OR CAST(photos AS TEXT) = ''")
        with op.batch_alter_table("part") as batch:
            batch.alter_column(
                "photos",
                existing_type=photos["type"],
                type_=PHOTOS_TYPE,
                nullable=False,
                server_default=sa.text("'[]'"),
                postgresql_using="photos::jsonb",
            )

    if bind.dialect.name == "sqlite":
        fks = sa.inspect(bind).get_foreign_keys("part")
        if any(fk["constrained_columns"] == ["car_id"] and fk.get("options", {}).get("ondelete") != "SET NULL" for fk in fks):
            with op.batch_alter_table(
                "part", recreate="always", naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s"}
            ) as batch:
                batch.drop_constraint("fk_part_car_id", type_="foreignkey")
                batch.create_foreign_key("part_car_id_fkey", "car", ["car_id"], ["id"], ondelete="SET NULL")
        return
    if bind.dialect.name != "postgresql":
        return
    for fk in inspector.get_foreign_keys("part"):
        if fk["constrained_columns"] == ["car_id"] and fk.get("options", {}).get("ondelete") != "SET NULL":
            op.drop_constraint(fk["name"], "part", type_="foreignkey")
            op.create_foreign_key("part_car_id_fkey", "part", "car", ["car_id"], ["id"], ondelete="SET NULL")


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    _add_missing_columns(inspector, "car", _car_columns())

    if inspector.has_table("part"):
        _add_missing_columns(inspector, "part", _part_columns())
        if "car_id" not in {column["name"] for column in inspector.get_columns("part")}:
            op.add_column("part", sa.Column("car_id", sa.Integer(), sa.ForeignKey("car.id", ondelete="SET NULL")))
        _normalize_legacy_part(bind, inspector)
    else:
        op.create_table("part", sa.Column("id", sa.Integer(), primary_key=True), *_part_columns())

    op.execute("UPDATE car SET status = 'available' WHERE status IS NULL")
    op.execute("UPDATE car SET mileage = 0 WHERE mileage IS NULL")
    with op.batch_alter_table("car") as batch:
        batch.alter_column("status", existing_type=sa.String(length=50), nullable=False)
        batch.alter_column("mileage", existing_type=sa.Integer(), nullable=False)

    # Empty strings would violate the partial unique indexes below.
    op.execute("UPDATE car SET vin = NULL WHERE TRIM(vin) = ''")
    op.execute("UPDATE part SET sku = NULL WHERE TRIM(sku) = ''")

    inspector = sa.inspect(bind)
    _create_index_if_missing(
        inspector, "uq_car_vin", "car", ["vin"], unique=True,
        postgresql_where=sa.text("vin IS NOT NULL"), sqlite_where=sa.text("vin IS NOT NULL"),
    )
    _create_index_if_missing(
        inspector, "uq_part_sku", "part", ["sku"], unique=True,
        postgresql_where=sa.text("sku IS NOT NULL"), sqlite_where=sa.text("sku IS NOT NULL"),
    )
    _create_index_if_missing(inspector, "ix_part_name", "part", ["name"])
    _create_index_if_missing(inspector, "ix_part_car_id", "part", ["car_id"])

    if bind.dialect.name == "postgresql":
        op.execute(
            """
            CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER LANGUAGE plpgsql AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$;
            """
        )
        for table in ("car", "part"):
            op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table}")
            op.execute(
                f"CREATE TRIGGER trg_{table}_updated_at BEFORE UPDATE ON {table} "
                f"FOR EACH ROW EXECUTE FUNCTION set_updated_at()"
            )


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in ("car", "part"):
            op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table}")
        op.execute("DROP FUNCTION IF EXISTS set_updated_at()")
    op.drop_index("uq_car_vin", table_name="car")
    op.drop_table("part")
    op.drop_column("car", "updated_at")
    op.drop_column("car", "created_at")
