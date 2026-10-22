from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class PartBase(SQLModel):
    name: str
    category: Optional[str] = None
    sku: Optional[str] = None
    quantity: int = 0
    price: Optional[float] = 0.0
    description: Optional[str] = None
    car_id: Optional[int] = Field(default=None, foreign_key="car.id")


class Part(PartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    car: Optional["Car"] = Relationship(back_populates="parts")


class PartCreate(PartBase):
    pass


class PartRead(PartBase):
    id: int


class PartUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
