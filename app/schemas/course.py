from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    description: str
    duration: str


class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    duration: str

    class Config:
        from_attributes = True