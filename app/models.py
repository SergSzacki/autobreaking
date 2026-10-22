from typing import Optional

from sqlmodel import Field, SQLModel


class CarBase(SQLModel):
    make: str
    model: str
    year: int
    vin: Optional[str] = None
    mileage: Optional[int] = 0
    color: Optional[str] = None
    status: Optional[str] = "available"


class Car(CarBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id: int


class CarUpdate(SQLModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vin: Optional[str] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    status: Optional[str] = None


class PartBase(SQLModel):
    name: str
    category: Optional[str] = None
    sku: Optional[str] = None
    quantity: int = 0
    min_quantity: int = 0
    price: Optional[float] = 0
    supplier: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    car_id: Optional[int] = Field(default=None, foreign_key="car.id")


class Part(PartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


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
    car_id: Optional[int] = None
