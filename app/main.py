from fastapi import (FastAPI, Depends,
                     HTTPException, Header)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app.database import Base, engine, get_db
from app import models
from app.security import decode_token
from app.api import auth, routes, stages, events, analytics, notifications

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Target Route API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_methods=[""],
    allow_headers=["*"],
)


def get_current_user(
        authorization: Optional[str] = Header(None),
        db: Session = Depends(get_db),
) -> models.User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Нет токена")


token = authorization.split(" ", 1)[1]
payload = decode_token(token)
if not payload:
    raise HTTPException(status_code=401, detail="Невалидный токен")
user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
if not user:
    raise HTTPException(status_code=401, detail="Пользователь не найден")
return user
app.include_router(auth.router, prefix="/api")
app.include_router(routes.router, prefix="/api")
app.include_router(stages.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "Target Route API"}
