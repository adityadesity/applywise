from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)

    skills = Column(JSON, nullable=True)

    roles = Column(JSON, nullable=True)

    education = Column(JSON, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    experience_years = Column(
    Integer,
    nullable=True
    )

    preferred_roles = Column(
        JSON,
        nullable=True
    )

    preferred_locations = Column(
        JSON,
        nullable=True
    )

    expected_ctc = Column(
        Integer,
        nullable=True
    )
    user = relationship("User")