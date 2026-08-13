from pydantic import BaseModel, EmailStr, Field, field_validator,ConfigDict


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Enter your username"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Enter your password"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\"

        if not any(char in special_characters for char in value):
            raise ValueError("Password must contain at least one special character")

        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role:str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Enter your password"
    )