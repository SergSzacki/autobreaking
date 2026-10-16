from sqlalchemy import Numeric
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    vin: Mapped[str | None] = mapped_column(
        String(17),
        nullable=True
    )

    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    purchase_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE"
    )