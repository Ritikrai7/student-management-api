from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.student import Student
from app.routers import user,student,course,enrollment,attendance,assignment,notification,activity_log
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.assignment import Assignment
from app.models.notification import Notification
from app.models.activity_log import ActivityLog

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(attendance.router)
app.include_router(assignment.router)
app.include_router(notification.router)
app.include_router(activity_log.router)

@app.get("/")
def home():
    return {"message": "Student Management API"}