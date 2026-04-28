from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.candidate_profile import (
    CandidateProfile
)
from app.schemas.profile import CompleteProfileRequest

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(
        CandidateProfile
    ).filter(
        CandidateProfile.user_id ==
        current_user.id
    ).first()

    return profile

@router.patch("/complete")
def complete_profile(
    data: CompleteProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    profile = db.query(
        CandidateProfile
    ).filter(
        CandidateProfile.user_id ==
        current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    profile.experience_years = (
        data.experience_years
    )

    profile.preferred_roles = (
        data.preferred_roles
    )

    profile.preferred_locations = (
        data.preferred_locations
    )

    profile.expected_ctc = (
        data.expected_ctc
    )

    db.commit()
    db.refresh(profile)

    return profile


@router.patch("/complete")
def complete_profile(
    data: CompleteProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    profile = db.query(
        CandidateProfile
    ).filter(
        CandidateProfile.user_id ==
        current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    profile.experience_years = (
        data.experience_years
    )

    profile.preferred_roles = (
        data.preferred_roles
    )

    profile.preferred_locations = (
        data.preferred_locations
    )

    profile.expected_ctc = (
        data.expected_ctc
    )

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile completed successfully",
        "profile": profile
    }