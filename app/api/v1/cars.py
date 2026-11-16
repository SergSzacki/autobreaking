from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, or_
from sqlmodel import Session, select

from app.core.database import get_session
from app.models import Car, CarCreate, CarListResponse, CarRead, CarUpdate, Part, PartCreate, PartRead, PartUpdate

router = APIRouter(prefix="/cars", tags=["cars"])


def get_car_or_404(session: Session, car_id: int) -> Car:
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


def get_car_part_or_404(session: Session, car_id: int, part_id: int) -> Part:
    part = session.get(Part, part_id)
    if not part or part.car_id != car_id:
        raise HTTPException(status_code=404, detail="Part not found")
    return part


@router.get("", response_model=CarListResponse)
def list_cars(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=200),
    q: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    statement = select(Car)
    if q and q.strip():
        q_like = f"%{q.strip()}%"
        statement = statement.where(
            or_(Car.make.ilike(q_like), Car.model.ilike(q_like), Car.vin.ilike(q_like))
        )

    total = session.exec(select(func.count()).select_from(statement.subquery())).one()
    cars = session.exec(
        statement.order_by(Car.id).offset((page - 1) * per_page).limit(per_page)
    ).all()

    return {"cars": cars, "meta": {"page": page, "per_page": per_page, "total": total}}


@router.get("/{car_id}", response_model=CarRead)
def get_car(car_id: int, session: Session = Depends(get_session)):
    return get_car_or_404(session, car_id)


@router.post("", response_model=CarRead, status_code=201)
def create_car(car_in: CarCreate, session: Session = Depends(get_session)):
    car = Car.model_validate(car_in)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


def _apply_car_update(session: Session, car: Car, data: dict) -> Car:
    car.sqlmodel_update(data)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


@router.put("/{car_id}", response_model=CarRead)
def update_car(car_id: int, car_in: CarCreate, session: Session = Depends(get_session)):
    car = get_car_or_404(session, car_id)
    return _apply_car_update(session, car, car_in.model_dump())


@router.patch("/{car_id}", response_model=CarRead)
def patch_car(car_id: int, car_in: CarUpdate, session: Session = Depends(get_session)):
    car = get_car_or_404(session, car_id)
    return _apply_car_update(session, car, car_in.model_dump(exclude_unset=True))


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int, session: Session = Depends(get_session)):
    car = get_car_or_404(session, car_id)
    session.delete(car)
    session.commit()
    return Response(status_code=204)


@router.get("/{car_id}/parts", response_model=list[PartRead])
def list_car_parts(car_id: int, session: Session = Depends(get_session)):
    get_car_or_404(session, car_id)
    statement = select(Part).where(Part.car_id == car_id).order_by(Part.name)
    return session.exec(statement).all()


@router.get("/{car_id}/parts/{part_id}", response_model=PartRead)
def get_car_part(car_id: int, part_id: int, session: Session = Depends(get_session)):
    return get_car_part_or_404(session, car_id, part_id)


@router.post("/{car_id}/parts", response_model=PartRead, status_code=201)
def create_car_part(car_id: int, part_in: PartCreate, session: Session = Depends(get_session)):
    get_car_or_404(session, car_id)
    part = Part.model_validate(part_in, update={"car_id": car_id})
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@router.patch("/{car_id}/parts/{part_id}", response_model=PartRead)
def patch_car_part(car_id: int, part_id: int, part_in: PartUpdate, session: Session = Depends(get_session)):
    part = get_car_part_or_404(session, car_id, part_id)
    data = part_in.model_dump(exclude_unset=True)
    if data.get("car_id") is not None:
        get_car_or_404(session, data["car_id"])
    part.sqlmodel_update(data)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@router.delete("/{car_id}/parts/{part_id}", status_code=204)
def delete_car_part(car_id: int, part_id: int, session: Session = Depends(get_session)):
    part = get_car_part_or_404(session, car_id, part_id)
    session.delete(part)
    session.commit()
    return Response(status_code=204)
