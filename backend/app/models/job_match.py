from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    JSON
)

from app.db.base import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    score = Column(
        Integer,
        nullable=False
    )

    matched_skills = Column(
        JSON,
        nullable=True
    )

    missing_skills = Column(
        JSON,
        nullable=True
    )

    reasoning = Column(
        Text,
        nullable=False
    )