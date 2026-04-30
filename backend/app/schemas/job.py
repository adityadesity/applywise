from pydantic import BaseModel
from typing import Optional


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    apply_url: str
    source: str