import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.utils.resume_parser import (
    extract_text_from_pdf
)
from app.db.deps import get_db
from app.api.deps import get_current_user

from app.models.user import User
from app.models.resume import Resume
from app.models.candidate_profile import (
    CandidateProfile
)

from app.services.profile_extractor import (
    extract_candidate_profile
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = "uploads"


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    # Create uploads directory if not exists
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    # Fixed filename per user (overwrite old file)
    filename = (
        f"user_{current_user.id}_resume.pdf"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Save uploaded file
    with open(
        file_path,
        "wb"
    ) as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract raw text from PDF
    extracted_text = extract_text_from_pdf(
        file_path
    )

    # Extract structured AI data
    profile_data = extract_candidate_profile(
        extracted_text
    )

    # Check existing resume
    existing_resume = db.query(
        Resume
    ).filter(
        Resume.user_id == current_user.id
    ).first()

    # Update existing resume
    if existing_resume:
        existing_resume.file_path = file_path
        existing_resume.extracted_text = (
            extracted_text
        )
        resume = existing_resume

    # Create new resume
    else:
        resume = Resume(
            file_path=file_path,
            extracted_text=extracted_text,
            user_id=current_user.id
        )

        db.add(resume)

    # Check existing candidate profile
    existing_profile = db.query(
        CandidateProfile
    ).filter(
        CandidateProfile.user_id ==
        current_user.id
    ).first()

    # Update ONLY AI-owned fields
    if existing_profile:
        existing_profile.skills = (
            profile_data.get("skills")
        )

        existing_profile.roles = (
            profile_data.get("roles")
        )

        existing_profile.education = (
            profile_data.get("education")
        )

        candidate_profile = (
            existing_profile
        )

    # Create new candidate profile
    else:
        candidate_profile = (
            CandidateProfile(
                skills=profile_data.get(
                    "skills"
                ),
                roles=profile_data.get(
                    "roles"
                ),
                education=profile_data.get(
                    "education"
                ),
                user_id=current_user.id
            )
        )

        db.add(candidate_profile)

    # Save all changes
    db.commit()

    # Refresh objects
    db.refresh(resume)
    db.refresh(candidate_profile)

    return {
        "message": (
            "Resume uploaded successfully"
        ),
        "resume_id": resume.id
    }