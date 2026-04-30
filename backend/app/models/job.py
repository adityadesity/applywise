from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float
)

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    company = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    salary_min = Column(
        Float,
        nullable=True
    )

    salary_max = Column(
        Float,
        nullable=True
    )

    apply_url = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )