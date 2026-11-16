from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import field_validator
from sqlalchemy import JSON, Index, Numeric, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from .car import blank_to_none, timestamp_field

if TYPE_CHECKING:
    from .car import Car


PhotosType = JSON().with_variant(JSONB(), "postgresql")
PriceType = Numeric(12, 2, asdecimal=False)

_OPTIONAL_TEXT_FIELDS = ("category", "sku", "supplier", "location", "notes", "description")


def zero_if_blank(value: Any) -> Any:
    return 0 if value in (None, "") else value


class PartBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, index=True)
    category: Optional[str] = Field(default=None, max_length=100)
    sku: Optional[str] = Field(default=None, max_length=100)
    quantity: int = Field(default=0, ge=0)
    min_quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0, sa_type=PriceType)
    supplier: Optional[str] = Field(default=None, max_length=255)
    location: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = Field(default=None, sa_type=Text)
    description: Optional[str] = Field(default=None, sa_type=Text)
    photos: list[str] = Field(default_factory=list, sa_type=PhotosType)
    car_id: Optional[int] = Field(default=None, foreign_key="car.id", ondelete="SET NULL", index=True)

    @field_validator(*_OPTIONAL_TEXT_FIELDS, mode="before")
    @classmethod
    def _blank_to_none(cls, value: Any) -> Any:
        return blank_to_none(value)

    @field_validator("quantity", "min_quantity", "price", mode="before")
    @classmethod
    def _zero_if_blank(cls, value: Any) -> Any:
        return zero_if_blank(value)

    @field_validator("photos", mode="before")
    @classmethod
    def _photos_list(cls, value: Any) -> Any:
        return [] if value is None else value


class Part(PartBase, table=True):
    __table_args__ = (
        Index("uq_part_sku", "sku", unique=True,
              postgresql_where=text("sku IS NOT NULL"), sqlite_where=text("sku IS NOT NULL")),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = timestamp_field()
    updated_at: Optional[datetime] = timestamp_field()
    car: Optional["Car"] = Relationship(back_populates="parts")


class PartCreate(PartBase):
    pass


class PartRead(PartBase):
    id: int


class PartUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    sku: Optional[str] = Field(default=None, max_length=100)
    quantity: Optional[int] = Field(default=None, ge=0)
    min_quantity: Optional[int] = Field(default=None, ge=0)
    price: Optional[float] = Field(default=None, ge=0)
    supplier: Optional[str] = Field(default=None, max_length=255)
    location: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[list[str]] = None
    car_id: Optional[int] = None

    @field_validator(*_OPTIONAL_TEXT_FIELDS, mode="before")
    @classmethod
    def _blank_to_none(cls, value: Any) -> Any:
        return blank_to_none(value)

    @field_validator("quantity", "min_quantity", "price", mode="before")
    @classmethod
    def _zero_if_blank(cls, value: Any) -> Any:
        return zero_if_blank(value)


class InventoryItem(PartRead):
    make: Optional[str] = None
    model: Optional[str] = None
