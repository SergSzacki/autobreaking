from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import field_validator
from sqlalchemy import DateTime, Index, String, func, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .part import Part


def timestamp_field() -> Any:
    return Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now(), "nullable": False},
    )


def blank_to_none(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


class CarBase(SQLModel):
    make: str = Field(min_length=1, max_length=255)
    model: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1886, le=2200)
    vin: Optional[str] = Field(default=None, max_length=17, sa_type=String(255))
    mileage: int = Field(default=0, ge=0)
    color: Optional[str] = Field(default=None, max_length=100)
    status: str = Field(default="available", max_length=50)

    @field_validator("vin", "color", mode="before")
    @classmethod
    def _blank_to_none(cls, value: Any) -> Any:
        return blank_to_none(value)

    @field_validator("mileage", mode="before")
    @classmethod
    def _default_mileage(cls, value: Any) -> Any:
        return 0 if value in (None, "") else value

    @field_validator("status", mode="before")
    @classmethod
    def _default_status(cls, value: Any) -> Any:
        return blank_to_none(value) or "available"


class Car(CarBase, table=True):
    __table_args__ = (
        Index("uq_car_vin", "vin", unique=True,
              postgresql_where=text("vin IS NOT NULL"), sqlite_where=text("vin IS NOT NULL")),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = timestamp_field()
    updated_at: Optional[datetime] = timestamp_field()
    parts: list["Part"] = Relationship(back_populates="car")


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id: int


class CarUpdate(SQLModel):
    make: Optional[str] = Field(default=None, min_length=1, max_length=255)
    model: Optional[str] = Field(default=None, min_length=1, max_length=255)
    year: Optional[int] = Field(default=None, ge=1886, le=2200)
    vin: Optional[str] = Field(default=None, max_length=17)
    mileage: Optional[int] = Field(default=None, ge=0)
    color: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None, max_length=50)

    @field_validator("vin", "color", mode="before")
    @classmethod
    def _blank_to_none(cls, value: Any) -> Any:
        return blank_to_none(value)


class CarListMeta(SQLModel):
    page: int
    per_page: int
    total: int


class CarListResponse(SQLModel):
    cars: list[CarRead]
    meta: CarListMeta
