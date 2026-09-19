from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogResponse


router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"]
)


@router.post("/", response_model=ActivityLogResponse)
def create_activity_log(
    activity: ActivityLogCreate,
    db: Session = Depends(get_db)
):
    new_log = ActivityLog(
        user_id=activity.user_id,
        action=activity.action,
        description=activity.description
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

@router.get("/", response_model=list[ActivityLogResponse])
def get_activity_logs(
    db: Session = Depends(get_db)
):
    logs = db.query(ActivityLog).all()

    return logs

@router.get("/user/{user_id}", response_model=list[ActivityLogResponse])
def get_user_activity_logs(
    user_id: int,
    db: Session = Depends(get_db)
):
    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user_id)
        .all()
    )

    return logs