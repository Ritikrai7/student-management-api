from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =========================
# User Registration
# =========================

@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Check duplicate username
    existing_username = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    # Save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# User Login
# =========================

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    # User not found
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    password_correct = verify_password(
        form_data.password,
        existing_user.hashed_password
    )

    # Password incorrect
    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT access token
    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# Current User
# =========================

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user