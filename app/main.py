from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.student import Student
from app.routers import user,student

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(student.router)


@app.get("/")
def home():
    return {"message": "Student Management API"}