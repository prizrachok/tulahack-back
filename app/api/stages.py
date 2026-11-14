from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/stages", tags=["stages"])

@router.patch("/{stage_id}", response_model=schemas.StageOut)
def update_stage(
    stage_id: int,
    body: schemas.StageUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Этап не найден")

    if body.status == "completed":
        prev = (
            db.query(models.Stage)
            .filter(
                models.Stage.route_id == stage.route_id,
                models.Stage.order < stage.order,
                models.Stage.status != "completed",
            )
            .first()
        )
        if prev:
            raise HTTPException(status_code=400, detail=f"Сначала завершите этап: {prev.title}")

    if body.status is not None:
        stage.status = body.status
    if body.comment is not None:
        stage.comment = body.comment

    db.add(models.Event(
        route_id=stage.route_id,
        stage_id=stage.id,
        actor_id=current_user.id,
        event_type="stage_updated",
        description=f"Этап «{stage.title}» → {stage.status}",
    ))
    db.commit()
    db.refresh(stage)
    return stage