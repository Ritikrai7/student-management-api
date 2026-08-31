from pydantic import BaseModel
from datetime import date


class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: str


class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    date: date
    status: str

    class Config:
        from_attributes = True