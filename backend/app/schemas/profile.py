from pydantic import BaseModel
from typing import List, Optional


class CompleteProfileRequest(
    BaseModel
):
    experience_years: int
    preferred_roles: List[str]
    preferred_locations: List[str]
    expected_ctc: Optional[float] = None