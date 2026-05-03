from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.job import Job
from app.schemas.job import JobCreate
from app.api.deps import (
    get_current_user
)

from app.models.user import User
from app.models.candidate_profile import (
    CandidateProfile
)

from app.services.job_matcher import (
    match_candidate_to_job
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)
from app.models.job_match import (
    JobMatch
)



from app.models.user import User

@router.post("/")
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        apply_url=job_data.apply_url,
        source=job_data.source
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(
        Job
    ).all()

    return jobs

@router.get("/recommendations")
def get_recommendations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    matches = (
    db.query(
        JobMatch,
        Job
    )
    .join(
        Job,
        JobMatch.job_id == Job.id
    )
    .filter(
        JobMatch.user_id == current_user.id
    )
    .order_by(
        JobMatch.score.desc()
    )
    .offset(skip)
    .limit(limit)
    .all()
    )
    results = []

    for match, job in matches:
        results.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "apply_url": job.apply_url,
            "source": job.source,
            "match_score": match.score,
            "matched_skills": match.matched_skills,
            "missing_skills": match.missing_skills,
            "reasoning": match.reasoning
        })

    return results
@router.get("/recommendations/{job_id}")
def get_recommendation_details(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    recommendation = (
        db.query(
            JobMatch
        )
        .filter(
            JobMatch.user_id == current_user.id,
            JobMatch.job_id == job_id
        )
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    job = (
        db.query(
            Job
        )
        .filter(
            Job.id == job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "apply_url": job.apply_url,
        "source": job.source,
        "match_score": recommendation.score,
        "matched_skills": recommendation.matched_skills,
        "missing_skills": recommendation.missing_skills,
        "reasoning": recommendation.reasoning
    }

@router.post("/recommendations/refresh")
def refresh_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return match_all_jobs(
        db=db,
        current_user=current_user
    )
@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(
        Job
    ).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


@router.post("/{job_id}/match")
def match_job(
    job_id: int,
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

    job = db.query(
        Job
    ).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    candidate_data = {
        "skills": profile.skills,
        "roles": profile.roles,
        "education": profile.education,
        "experience_years":
        profile.experience_years,
        "preferred_roles":
        profile.preferred_roles,
        "preferred_locations":
        profile.preferred_locations,
        "expected_ctc":
        profile.expected_ctc
    }

    job_data = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max
    }

    match_result = (
        match_candidate_to_job(
            candidate_data,
            job_data
        )
    )

    return match_result




# Deprecating the api and making it as a utility function
# @router.post("/match-all")
def match_all_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    # Fetch candidate profile
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

    # Fetch all jobs
    jobs = db.query(
        Job
    ).all()

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail="No jobs found"
        )

    # Delete old matches
    db.query(
        JobMatch
    ).filter(
        JobMatch.user_id ==
        current_user.id
    ).delete()

    db.commit()

    candidate_data = {
        "skills": profile.skills,
        "roles": profile.roles,
        "education": profile.education,
        "experience_years":
        profile.experience_years,
        "preferred_roles":
        profile.preferred_roles,
        "preferred_locations":
        profile.preferred_locations,
        "expected_ctc":
        profile.expected_ctc
    }

    matched_results = []

    # Match every job
    for job in jobs:
        job_data = {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max
        }

        match_result = (
            match_candidate_to_job(
                candidate_data,
                job_data
            )
        )

        job_match = JobMatch(
            user_id=current_user.id,
            job_id=job.id,
            score=match_result["score"],
            matched_skills=match_result[
                "matched_skills"
            ],
            missing_skills=match_result[
                "missing_skills"
            ],
            reasoning=match_result[
                "reasoning"
            ]
        )

        db.add(job_match)

        matched_results.append({
            "job_id": job.id,
            "score":
            match_result["score"]
        })

    db.commit()

    # Sort highest score first
    matched_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "message":
        "Job matching completed",
        "matches":
        matched_results[:10]
    }

