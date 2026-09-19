from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollStudent
from app.models.student import Student
from app.models.course import Course


router = APIRouter(
    prefix="/enrollment",
    tags=["Enrollment"]
)


@router.post("/")
def enroll_student(
    enrollment: EnrollStudent,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = db.query(Course).filter(
        Course.id == enrollment.course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

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

@router.get("/")
def get_enrolled_students(
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enrollment).all()

    return [
        {
            "student_id": enrollment.student_id,
            "student_name": enrollment.student.name,
            "course_id": enrollment.course_id,
            "course_name": enrollment.course.name
        }
        for enrollment in enrollments
    ]

@router.get("/student/{student_id}")
def get_student_enrollments(
    student_id: int,
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

    return [
        {
            "student_id": enrollment.student_id,
            "student_name": enrollment.student.name,
            "course_id": enrollment.course_id,
            "course_name": enrollment.course.name
        }
        for enrollment in enrollments
    ]

@router.get("/course/{course_id}")
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).all()

    return [
        {
            "student_id": enrollment.student_id,
            "student_name": enrollment.student.name,
            "course_id": enrollment.course_id,
            "course_name": enrollment.course.name
        }
        for enrollment in enrollments
    ]

@router.delete("/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    db.delete(enrollment)
    db.commit()

    return {
        "message": "Enrollment deleted successfully",
        "enrollment_id": enrollment_id
    }