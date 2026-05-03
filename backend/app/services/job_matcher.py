from pydantic import BaseModel
from typing import List

from langchain_core.output_parsers import (
    PydanticOutputParser
)

from app.core.llm import llm


class JobMatchSchema(
    BaseModel
):
    score: int
    matched_skills: List[str]
    missing_skills: List[str]
    reasoning: str


parser = PydanticOutputParser(
    pydantic_object=JobMatchSchema
)


def match_candidate_to_job(
    candidate_profile: dict,
    job: dict
):
    format_instructions = (
        parser.get_format_instructions()
    )

    prompt = f"""
        Match this candidate with this job.

        Evaluate based on:

        1. Skills match
        2. Role relevance
        3. Experience fit
        4. Location preference
        5. Salary expectation

        Return a score from 0 to 100.
        In reasoning section, use first person as if you are telling the candidate. Keep it very short and crisp.

        {format_instructions}

        Candidate Profile:
        {candidate_profile}

        Job:
        {job}
        """

    response = llm.invoke(
        prompt
    )

    parsed_output = parser.parse(
        response.content
    )

    return parsed_output.model_dump()