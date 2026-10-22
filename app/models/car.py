from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


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
    parts: list["Part"] = Relationship(back_populates="car")


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
