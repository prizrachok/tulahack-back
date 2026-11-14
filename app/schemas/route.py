from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RouteCreate(BaseModel):
      title: str
      student_id: int
      organization_id: Optional[int] = None
      program_id: Optional[int] = None

class RouteOut(BaseModel):
      id: int
      title: str
      student_id: int
      organization_id: Optional[int] = None
      rogram_id: Optional[int] = None
      status: str
      prof_test_result: Optional[str] = None
      created_at: datetime
      updated_at: datetime

class Config:
    from_attributes = True
class StageOut(BaseModel):
      id: int
      route_id: int
      stage_type: str
      title: str
      description: Optional[str] = None
      order: int
      status: str
      due_date: Optional[str] = None
      comment: Optional[str] = None

class Config:
    from_attributes = True


class StageUpdate(BaseModel):
      status: Optional[str] = None
      comment: Optional[str] = None

class EventCreate(BaseModel):
      event_type: str
      description: str
      stage_id: Optional[int] = None

class EventOut(BaseModel):
      id: int
      route_id: int
      stage_id: Optional[int] = None
      actor_id: Optional[int] = None
      event_type: str
      description: str
      created_at: datetime

class Config:
    from_attributes = True
