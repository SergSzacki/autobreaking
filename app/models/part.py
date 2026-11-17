import json
from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from sqlmodel import Field, Relationship, SQLModel


class PhotoListType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return []

        try:
            photos = json.loads(value)
        except (TypeError, ValueError):
            return [value]

        if isinstance(photos, str):
            return [photos] if photos else []
        if isinstance(photos, list):
            return [photo for photo in photos if isinstance(photo, str)]
        return []


class PartBase(SQLModel):
    name: str
    category: Optional[str] = None
    sku: Optional[str] = None
    quantity: int = 0
    min_quantity: int = 0
    price: Optional[float] = 0.0
    supplier: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    description: Optional[str] = None
    photos: List[str] = Field(default_factory=list, sa_type=PhotoListType())
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
    min_quantity: Optional[int] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
