from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_current_user
get_current_user()


from sqlalchemy.sql.functions import user

import app
from app.database import Base, engine, get_db
from app import models
from app.models import User
from app.security import decode_token
from app.api import (auth, routes,
stages, events, analytics,
notifications)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Target Route API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#Подключаем все роутеры под /api
app.include_router(auth.router, prefix="/api")
app.include_router(routes.router, prefix="/api")
app.include_router(stages.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "message":
"Target Route API"}