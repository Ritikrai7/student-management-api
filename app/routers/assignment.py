from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.dependencies import get_db
from app.models.assignment import Assignment
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse
)


router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)


@router.post("/", response_model=AssignmentResponse)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db)
):
    new_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        due_date=assignment.due_date,
        course_id=assignment.course_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment

@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    assignment: AssignmentUpdate,
    db: Session = Depends(get_db)
):
    existing_assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    existing_assignment.title = assignment.title
    existing_assignment.description = assignment.description
    existing_assignment.due_date = assignment.due_date
    existing_assignment.course_id = assignment.course_id

    db.commit()
    db.refresh(existing_assignment)

    return existing_assignment

@router.get("/", response_model=list[AssignmentResponse])
def get_assignments(
    db: Session = Depends(get_db)
):
    assignments = db.query(Assignment).all()

    return assignments

@router.get("/course/{course_id}", response_model=list[AssignmentResponse])
def get_course_assignments(
    course_id: int,
    db: Session = Depends(get_db)
):
    assignments = db.query(Assignment).filter(
        Assignment.course_id == course_id
    ).all()

    return assignments

@router.get(
    "/student/{student_id}",
    response_model=list[AssignmentResponse]
)
def get_student_assignments(
    student_id: int,
    db: Session = Depends(get_db)
):
    assignments = (
        db.query(Assignment)
        .join(
            Enrollment,
            Assignment.course_id == Enrollment.course_id
        )
        .filter(
            Enrollment.student_id == student_id
        )
        .all()
    )

    return assignments

@router.get("/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    return assignment

@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    db.delete(assignment)
    db.commit()

    return {
        "message": "Assignment deleted successfully",
        "assignment_id": assignment_id
    }
