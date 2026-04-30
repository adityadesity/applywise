from dotenv import load_dotenv

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)


load_dotenv()


llm_client = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=1000
)


llm = ChatHuggingFace(
    llm=llm_client
)