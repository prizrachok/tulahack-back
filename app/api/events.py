from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/routes", tags=["events"])


@router.get("/{route_id}/events", response_model=list[schemas.EventOut])
def list_events(
    route_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Event)
        .filter(models.Event.route_id == route_id)
        .order_by(models.Event.created_at.desc())
        .all()
    )


@router.post("/{route_id}/events", response_model=schemas.EventOut)
def add_event(
    route_id: int,
    body: schemas.EventCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not db.query(models.Route).filter(models.Route.id == route_id).first():
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    event = models.Event(
        route_id=route_id,
        stage_id=body.stage_id,
        actor_id=current_user.id,
        event_type=body.event_type,
        description=body.description,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event