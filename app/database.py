from sqlalchemy import inspect, text
from sqlmodel import create_engine, SQLModel
from app.core.config import settings

connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args
)

def init_db():
    SQLModel.metadata.create_all(engine)

    with engine.begin() as connection:
        columns = {
            column["name"]
            for column in inspect(connection).get_columns("part")
        }
        new_columns = {
            "min_quantity": "INTEGER NOT NULL DEFAULT 0",
            "supplier": "VARCHAR",
            "location": "VARCHAR",
            "notes": "VARCHAR",
        }
        for name, column_type in new_columns.items():
            if name not in columns:
                connection.execute(
                    text(f"ALTER TABLE part ADD COLUMN {name} {column_type}")
                )
