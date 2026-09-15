from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.notification import Notification
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# Create Notification
@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    new_notification = Notification(
        title=notification.title,
        message=notification.message,
        user_id=notification.user_id
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


# Get All Notifications
@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db)
):
    notifications = db.query(Notification).all()

    return notifications


# Get Notifications of a Specific User
@router.get("/user/{user_id}", response_model=list[NotificationResponse])
def get_user_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .all()
    )

    return notifications


# Get Unread Notifications of a Specific User
@router.get("/user/{user_id}/unread", response_model=list[NotificationResponse])
def get_unread_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .all()
    )

    return notifications


# Mark Notification as Read
@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read",
        "notification_id": notification.id
    }