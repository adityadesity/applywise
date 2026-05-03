from pydantic import BaseModel
from typing import List, Optional


class JobRecommendationResponse(BaseModel):
    job_id: int
    title: str
    company: str
    location: str
    description: str

    salary_min: Optional[int]
    salary_max: Optional[int]

    apply_url: str
    source: str

    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    reasoning: str