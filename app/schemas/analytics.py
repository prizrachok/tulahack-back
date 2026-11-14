from pydantic import BaseModel
from typing import Dict


class FunnelOut(BaseModel):
    total_routes: int
    by_stage: Dict[str, int]           # {"1": 0, "2": 1, ...}
    by_status: Dict[str, int]          # {"not_started": 5, "in_progress": 1}
    by_route_status: Dict[str, int]    # {"active": 1, "completed": 0}


class NotificationOut(BaseModel):
    id: int
    route_id: int
    event_type: str
    description: str
    created_at: str