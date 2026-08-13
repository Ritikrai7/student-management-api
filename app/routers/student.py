from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_roles
from app.schemas.student import StudentCreate, StudentResponse
from app.models.student import Student
from app.models.user import User


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# =========================
# Create Student
# =========================

@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

# =========================
# Update Student
# =========================

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = student_data.name
    student.email = student_data.email
    student.age = student_data.age
    student.course = student_data.course

    db.commit()
    db.refresh(student)

    return student


# =========================
# Get All Students
# =========================

@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    students = db.query(Student).all()

    return students


# =========================
# Get Student By ID
# =========================

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

# =========================
# Delete Student
# =========================

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    )
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }