from pydantic import BaseModel
from datetime import datetime


class ActivityLogCreate(BaseModel):
    user_id: int
    action: str
    description: str


class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True