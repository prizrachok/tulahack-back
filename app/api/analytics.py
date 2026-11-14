from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import Counter

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/funnel", response_model=schemas.FunnelOut)
def funnel(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    routes = db.query(models.Route).all()
    stages = db.query(models.Stage).all()

    by_stage = Counter()
    for s in stages:
        by_stage[str(s.order)] += 1

    by_status = Counter(s.status for s in stages)
    by_route_status = Counter(r.status for r in routes)

    return {
        "total_routes": len(routes),
        "by_stage": dict(by_stage),
        "by_status": dict(by_status),
        "by_route_status": dict(by_route_status),
    }