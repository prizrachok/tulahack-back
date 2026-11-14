from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.security import decode_token


def get_current_user(
        request: Request,
        db: Session = Depends(get_db),
) -> models.User:
    # Читаем заголовок напрямую из запроса
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Заголовок Authorization отсутствует")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Неверный формат заголовка. Ожидается 'Bearer <токен>'")

    # Отрезаем слово "Bearer " и берем токен
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")

    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user