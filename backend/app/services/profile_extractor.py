from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

from langchain_core.output_parsers import (
    PydanticOutputParser
)


load_dotenv()


class CandidateProfileSchema(BaseModel):
    skills: List[str]
    roles: List[str]
    education: List[str]


parser = PydanticOutputParser(
    pydantic_object=CandidateProfileSchema
)


llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=1000
)

model = ChatHuggingFace(
    llm=llm
)


def extract_candidate_profile(
    resume_text: str
):
    format_instructions = (
        parser.get_format_instructions()
    )

    prompt = f"""
    Extract candidate profile from resume.

    {format_instructions}

    Resume:
    {resume_text}
    """

    response = model.invoke(prompt)

    parsed_output = parser.parse(
        response.content
    )

    return parsed_output.model_dump()