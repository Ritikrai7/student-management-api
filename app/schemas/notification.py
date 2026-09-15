from pydantic import BaseModel
from datetime import datetime


class NotificationCreate(BaseModel):
    title: str
    message: str
    user_id: int


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True