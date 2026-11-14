from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
def my_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Простая логика: все события маршрутов, где пользователь — участник
    route_ids = []
    if current_user.role == "student":
        route_ids = [
            r.id for r in db.query(models.Route)
            .filter(models.Route.student_id == current_user.id).all()
        ]
    else:
        route_ids = [r.id for r in db.query(models.Route).all()]

    events = (
        db.query(models.Event)
        .filter(models.Event.route_id.in_(route_ids))
        .order_by(models.Event.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": e.id,
            "route_id": e.route_id,
            "event_type": e.event_type,
            "description": e.description,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in events
    ]