from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    VECTOR_DIR: str = "vectorstore_earnings"
    PROJECT_NAME: str = "earning_calls_transcripts_llm_agents"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8001",  # type: ignore
    ]
    SYSTEM_TEMPLATE: str = """
    Answer the user's questions based on the below context. 
    If the context doesn't contain any relevant information to the questions, don't make someting up
    and just reply information cannot be fount:
    <context>
    {context}
    </context>
    """

