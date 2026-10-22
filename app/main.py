from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Session, select

from app.database import engine, init_db
from app.models import Car, CarCreate, CarRead, CarUpdate, Part, PartCreate, PartRead, PartUpdate

app = FastAPI(title="AutoBreaking - Cars API")


@app.on_event("startup")
def on_startup():
    init_db()


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/cars", response_model=Dict)
def list_cars(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=200),
    q: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    statement = select(Car)
    if q:
        q_like = f"%{q}%"
        statement = statement.where(
            (Car.make.ilike(q_like)) | (Car.model.ilike(q_like)) | (Car.vin.ilike(q_like))
        )
    total = session.exec(select([Car]).where(statement._whereclause)).all() if q else session.exec(select(Car)).count()
    skip = (page - 1) * per_page
    cars = session.exec(statement.offset(skip).limit(per_page)).all()
    return {"cars": cars, "meta": {"page": page, "per_page": per_page, "total": len(cars) if q else total}}


@app.get("/api/cars/{car_id}", response_model=CarRead)
def get_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.post("/api/cars", response_model=CarRead, status_code=201)
def create_car(car_in: CarCreate, session: Session = Depends(get_session)):
    car = Car.from_orm(car_in)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@app.put("/api/cars/{car_id}", response_model=CarRead)
def update_car(car_id: int, car_in: CarCreate, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car.make = car_in.make
    car.model = car_in.model
    car.year = car_in.year
    car.vin = car_in.vin
    car.mileage = car_in.mileage
    car.color = car_in.color
    car.status = car_in.status
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@app.patch("/api/cars/{car_id}", response_model=CarRead)
def patch_car(car_id: int, car_in: CarUpdate, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car_data = car_in.dict(exclude_unset=True)
    for key, value in car_data.items():
        setattr(car, key, value)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@app.delete("/api/cars/{car_id}", status_code=204)
def delete_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    session.delete(car)
    session.commit()
    return


@app.get("/api/cars/{car_id}/parts", response_model=List[PartRead])
def list_car_parts(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    statement = select(Part).where(Part.car_id == car_id)
    return session.exec(statement).all()


@app.get("/api/cars/{car_id}/parts/{part_id}", response_model=PartRead)
def get_car_part(car_id: int, part_id: int, session: Session = Depends(get_session)):
    part = session.get(Part, part_id)
    if not part or part.car_id != car_id:
        raise HTTPException(status_code=404, detail="Part not found")
    return part


@app.post("/api/cars/{car_id}/parts", response_model=PartRead, status_code=201)
def create_car_part(car_id: int, part_in: PartCreate, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    part = Part.from_orm(part_in)
    part.car_id = car_id
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@app.patch("/api/cars/{car_id}/parts/{part_id}", response_model=PartRead)
def patch_car_part(car_id: int, part_id: int, part_in: PartUpdate, session: Session = Depends(get_session)):
    part = session.get(Part, part_id)
    if not part or part.car_id != car_id:
        raise HTTPException(status_code=404, detail="Part not found")
    for key, value in part_in.dict(exclude_unset=True).items():
        setattr(part, key, value)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@app.delete("/api/cars/{car_id}/parts/{part_id}", status_code=204)
def delete_car_part(car_id: int, part_id: int, session: Session = Depends(get_session)):
    part = session.get(Part, part_id)
    if not part or part.car_id != car_id:
        raise HTTPException(status_code=404, detail="Part not found")
    session.delete(part)
    session.commit()
    return
