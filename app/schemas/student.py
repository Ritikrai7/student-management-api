from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Enter student name"
    )

    email: EmailStr

    age: int = Field(
        ...,
        ge=5,
        le=100,
        description="Enter student age"
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Enter student course"
    )


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str
    user_id:int

    model_config = {
        "from_attributes": True
    }