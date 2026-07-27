from pydantic_settings import BaseSettings
from pydantic import ValidationError
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeGuard Backend"
    DATABASE_URL: str = "sqlite:///./codeguard.db"
    LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
    
    GROQ_API_KEY: str | None = None
    FRONTEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:5500,http://127.0.0.1:3000,http://127.0.0.1:5500"
    
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    ESLINT_PATH: str = "eslint"

    # Score weights
    WEIGHT_CRITICAL: int = 30
    WEIGHT_HIGH: int = 20
    WEIGHT_MEDIUM: int = 10
    WEIGHT_LOW: int = 5

    class Config:
        env_file = str(BASE_DIR / ".env")
        extra = "ignore"

settings = Settings()