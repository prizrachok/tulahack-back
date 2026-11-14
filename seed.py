from app.database import SessionLocal, Base, engine
from app import models
from app.security import hash_password
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def upsert_user(email, password, full_name, role):
    u = db.query(models.User).filter(models.User.email == email).first()
    if u:
        return u
    u = models.User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
        is_active=True,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


student = upsert_user("student@test.ru", "12345678", "Иванов Иван", "student")
university = upsert_user("uni@test.ru", "12345678", "ТулГУ", "university")
company = upsert_user("company@test.ru", "12345678", "Ростех", "company")
admin = upsert_user("admin@test.ru", "12345678", "Администратор", "admin")

route = db.query(models.Route).first()
if not route:
    route = models.Route(
        title="Инженер-конструктор: ТулГУ → Ростех",
        student_id=student.id,
        organization_id=company.id,
        program_id=1,
        status="active",
        prof_test_result="Инженерное мышление, склонность к точным наукам",
    )
    db.add(route)
    db.commit()
    db.refresh(route)

    stage_defs = [
        ("career_guidance", "Профориентация", "Пройти тест на склонности"),
        ("university_choice", "Выбор вуза", "Выбрать направление и вуз"),
        ("contract", "Договор", "Подписать целевой договор"),
        ("education", "Обучение", "Учёба в вузе, сессии"),
        ("employment", "Трудоустройство", "Выход на работу"),
        ("retention", "Удержание", "Закрепление на предприятии"),
    ]
    for i, (stype, title, desc) in enumerate(stage_defs, start=1):
        db.add(models.Stage(
            route_id=route.id,
            stage_type=stype,
            title=title,
            description=desc,
            order=i,
            status="not_started",
            due_date=(datetime.utcnow() + timedelta(days=30 * i)).isoformat(),
        ))
    db.commit()

    first_stage = db.query(models.Stage).filter(
        models.Stage.route_id == route.id, models.Stage.order == 1
    ).first()
    first_stage.status = "in_progress"
    db.add(models.Event(
        route_id=route.id,
        stage_id=first_stage.id,
        actor_id=student.id,
        event_type="route_created",
        description="Маршрут создан, начата профориентация",
    ))
    db.commit()

print("✅ Seed завершён. Пользователи и маршрут созданы.")
db.close()