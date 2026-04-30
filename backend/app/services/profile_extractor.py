from pydantic import BaseModel
from typing import List

from langchain_core.output_parsers import (
    PydanticOutputParser
)

from app.core.llm import llm


class CandidateProfileSchema(
    BaseModel
):
    skills: List[str]
    roles: List[str]
    education: List[str]


parser = PydanticOutputParser(
    pydantic_object=CandidateProfileSchema
)


def extract_candidate_profile(
    resume_text: str
):
    format_instructions = (
        parser.get_format_instructions()
    )

    prompt = f"""
        Extract candidate profile from the resume.

        {format_instructions}

        Resume:
        {resume_text}
        """

    response = llm.invoke(
        prompt
    )

    parsed_output = parser.parse(
        response.content
    )

    return parsed_output.model_dump()