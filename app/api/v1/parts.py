from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import or_
from sqlmodel import Session, select

from app.api.v1.cars import get_car_or_404
from app.core.database import get_session
from app.models import Car, InventoryItem, Part, PartCreate, PartRead, PartUpdate

router = APIRouter(tags=["parts"])


def get_part_or_404(session: Session, part_id: int) -> Part:
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part


@router.get("/inventory", response_model=list[InventoryItem])
def list_inventory(
    q: Optional[str] = Query(None, description="Search by part name, SKU, category, car make or model"),
    car_id: Optional[int] = Query(None),
    session: Session = Depends(get_session),
):
    statement = select(Part, Car).join(Car, Part.car_id == Car.id, isouter=True)
    if q and q.strip():
        q_like = f"%{q.strip()}%"
        statement = statement.where(
            or_(
                Part.name.ilike(q_like),
                Part.sku.ilike(q_like),
                Part.category.ilike(q_like),
                Car.make.ilike(q_like),
                Car.model.ilike(q_like),
            )
        )
    if car_id is not None:
        statement = statement.where(Part.car_id == car_id)

    rows = session.exec(statement.order_by(Part.name)).all()
    return [
        InventoryItem(
            **part.model_dump(),
            make=car.make if car else None,
            model=car.model if car else None,
        )
        for part, car in rows
    ]


@router.post("/parts", response_model=PartRead, status_code=201)
def create_part(part_in: PartCreate, session: Session = Depends(get_session)):
    if part_in.car_id is not None:
        get_car_or_404(session, part_in.car_id)
    part = Part.model_validate(part_in)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@router.get("/parts/{part_id}", response_model=PartRead)
def get_part(part_id: int, session: Session = Depends(get_session)):
    return get_part_or_404(session, part_id)


@router.patch("/parts/{part_id}", response_model=PartRead)
def patch_part(part_id: int, part_in: PartUpdate, session: Session = Depends(get_session)):
    part = get_part_or_404(session, part_id)
    data = part_in.model_dump(exclude_unset=True)
    if data.get("car_id") is not None:
        get_car_or_404(session, data["car_id"])
    part.sqlmodel_update(data)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part


@router.delete("/parts/{part_id}", status_code=204)
def delete_part(part_id: int, session: Session = Depends(get_session)):
    part = get_part_or_404(session, part_id)
    session.delete(part)
    session.commit()
    return Response(status_code=204)
