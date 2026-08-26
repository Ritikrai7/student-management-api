from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=False
    )

    duration = Column(
        String(50),
        nullable=False
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )