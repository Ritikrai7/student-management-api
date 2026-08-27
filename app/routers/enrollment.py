from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollStudent


router = APIRouter(
    prefix="/enrollment",
    tags=["Enrollment"]
)


@router.post("/")
def enroll_student(
    enrollment: EnrollStudent,
    db: Session = Depends(get_db)
):
    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return {
        "message": "Student enrolled successfully",
        "enrollment_id": new_enrollment.id,
        "student_id": new_enrollment.student_id,
        "course_id": new_enrollment.course_id
    }