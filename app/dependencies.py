from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.config import settings
from app.models.user import User


# =========================
# OAuth2 Scheme
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


# =========================
# Database Dependency
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# Get Current User
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Get email from JWT
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Find user in database
    user = db.query(User).filter(
        User.email == email
    ).first()

    # User does not exist
    if user is None:
        raise credentials_exception

    # Check whether user is active
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user"
        )

    return user