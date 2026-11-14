from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,
                primary_key=True, index=True)
    email = Column(String, unique=True,
                   index=True, nullable=False)
    hashed_password = Column(String,
                             nullable=False)
    fullname = Column(String,
                      nullable=False)
    role = Column(String,
                  nullable=False)  # student/universiti/company/admin

    is_active = Column(Boolean,
                       default=True, )

    routes_as_student = relationship("Route",
                                     foreign_keys="Route.student_id",
                                     back_populates="student"
                                     )
    events = relationship("Event",
                          back_populates="actor")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    program_id = Column(Integer, nullable=True)
    status = Column(String, default="active")
    prof_test_result = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи для маршрута (ВОТ ЭТИ ТРИ СТРОЧКИ ДОЛЖНЫ БЫТЬ)
    student = relationship("User", foreign_keys=[student_id], back_populates="routes_as_student")
    stages = relationship("Stage", back_populates="route", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="route", cascade="all, delete-orphan")


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer,
                primary_key=True, index=True)
    route_id = Column(Integer,
                      ForeignKey("routes.id"),
                      nullable=False)
    stage_type = Column(String,
                        nullable=False)
    title = Column(String,
                   nullable=False)
    description = Column(Text,
                         nullable=True)
    order = Column(Integer,
                   nullable=False)
    status = Column(String,
                    default="not_started")
    due_date = Column(String,
                      nullable=True)
    comment = Column(Text,
                     nullable=True)

    route = relationship("Route",
                         back_populates="stages")

    class Event(Base):
        __tablename__ = "events"

        id = Column(Integer,
                    primary_key=True, index=True)
        route_id = Column(Integer,
                          ForeignKey("routes.id"),
                          nullable=False)
        stage_id = Column(Integer,
                          ForeignKey("stages.id"), nullable=True)
        actor_id = Column(Integer,
                          ForeignKey("users.id"), nullable=True)
        event_type = Column(String,
                            nullable=False)
        description = Column(Text,
                             nullable=False)
        created_at = Column(DateTime,
                            default=datetime.utcnow)

        route = relationship("Route",
                             back_populates="events")
        actor = relationship("User",
                             back_populates="events")
