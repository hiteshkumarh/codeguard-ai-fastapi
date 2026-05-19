from pydantic_settings import BaseSettings
from pydantic import ValidationError


import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeGuard Backend"
    DATABASE_URL: str = "sqlite:///./codeguard.db"
    LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
    
    # Read from environment variable safely
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY", None)
    
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    ESLINT_PATH: str = "eslint"

    # Score weights
    WEIGHT_CRITICAL: int = 30
    WEIGHT_HIGH: int = 20
    WEIGHT_MEDIUM: int = 10
    WEIGHT_LOW: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()