from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/")
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    new_attendance = Attendance(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {
        "message": "Attendance marked successfully",
        "attendance_id": new_attendance.id,
        "student_id": new_attendance.student_id,
        "date": new_attendance.date,
        "status": new_attendance.status
    }

@router.get("/{student_id}/statistics")
def attendance_statistics(
    student_id: int,
    db: Session = Depends(get_db)
):
    total_days = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).count()

    present_days = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.status == "Present"
    ).count()

    absent_days = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.status == "Absent"
    ).count()

    if total_days == 0:
        attendance_percentage = 0
    else:
        attendance_percentage = (
            present_days / total_days
        ) * 100

    return {
        "student_id": student_id,
        "total_days": total_days,
        "present": present_days,
        "absent": absent_days,
        "attendance_percentage": attendance_percentage
    }


@router.get("/{student_id}")
def get_student_attendance(
    student_id: int,
    db: Session = Depends(get_db)
):
    attendances = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    return attendances