from pydantic import BaseModel
from datetime import date


class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: date
    course_id: int


class AssignmentUpdate(BaseModel):
    title: str
    description: str
    due_date: date
    course_id: int


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: date
    course_id: int

    class Config:
        from_attributes = True