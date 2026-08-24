from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import func

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
        course=student.course,
        user_id=current_user.id
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
# Student Statistics
# =========================

@router.get("/statistics")
def student_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    total_students = db.query(func.count(Student.id)).filter(
        Student.is_deleted == False
    ).scalar()

    average_age = db.query(func.avg(Student.age)).filter(
            Student.is_deleted == False
        ).scalar()

    youngest_age = db.query(func.min(Student.age)).filter(
        Student.is_deleted == False
    ).scalar()

    oldest_age = db.query(func.max(Student.age)).filter(
        Student.is_deleted == False
    ).scalar()

    course_counts = db.query(
        Student.course,
        func.count(Student.id)
    ).filter(
        Student.is_deleted == False
    ).group_by(
        Student.course
    ).all()

    course_counts = {
    course: count
    for course, count in course_counts
    }

    return {
    "total_students": total_students,
    "average_age": average_age,
    "youngest_age": youngest_age,
    "oldest_age": oldest_age,
    "course_counts": course_counts
    }



# =========================
# Get All Students
# =========================

@router.get("/", response_model=list[StudentResponse])
def get_students(
    name: str | None = Query(default=None),
    course:str | None =Query(default=None),
    sort_by:str | None = Query(default=None),
    order:str = Query(default='asc'),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_roles("admin", "teacher")
    )
):
    query = db.query(Student).filter(
        Student.is_deleted==False
    )

    if sort_by and sort_by not in ["age", "name", "course"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by. Allowed values: age, name, course"
    )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Allowed values: asc, desc"
    )

    # Name search
    if name:
        query = query.filter(
            Student.name.ilike(f"%{name}%")
        )
    # course search
    if course:
        query=query.filter(
            Student.course==course
        )
    if sort_by == "age":
        if order == "desc":
            query = query.order_by(Student.age.desc())
        else:
            query = query.order_by(Student.age.asc())

    elif sort_by == "name":
        if order == "desc":
            query = query.order_by(Student.name.desc())
        else:
            query = query.order_by(Student.name.asc())

    elif sort_by == "course":
        if order == "desc":
            query = query.order_by(Student.course.desc())
        else:
            query = query.order_by(Student.course.asc())

    

    # Pagination
    offset = (page - 1) * limit

    students = query.offset(offset).limit(limit).all()

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
        Student.id == student_id,
        Student.is_deleted==False
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

    student.is_deleted=True
    db.commit()

    return {
        "message": "Student deleted successfully"
    }

# =========================
# Test User-Student Relationship
# =========================

@router.get("/user/{user_id}")
def get_user_students(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user.id,
        "username": user.username,
        "students": [
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "course": student.course
            }
            for student in user.students
            if not student.is_deleted
        ]
    }

# =========================
# Get Student's User
# =========================

@router.get("/{student_id}/user")
def get_student_user(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    user = student.user

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "student_id": student.id,
        "student_name": student.name,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }