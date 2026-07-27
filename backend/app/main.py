import os
from fastapi import FastAPI, Request
from app.api import router as api_router
from app.db.database import Base, engine
import app.models.analysis

# Create database tables
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CodeGuard Backend")

from app.core.config import settings

origins = [origin.strip() for origin in settings.FRONTEND_CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    from app.core.config import settings
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    
    if not settings.GROQ_API_KEY:
        logger.info("GROQ_API_KEY not set, AI features disabled")


