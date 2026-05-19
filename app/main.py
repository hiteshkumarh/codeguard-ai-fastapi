import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import routes
from app.database import Base, engine
import app.models.user_model  # Import user model to ensure table gets created by Base.metadata.create_all

# Create database tables
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CodeGuard Backend")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Only mount static if the directory exists (it will be created soon)
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.on_event("startup")
def startup_event():
    from app.config import settings
    from app.utils.logger import get_logger
    logger = get_logger(__name__)
    
    if not settings.GROQ_API_KEY:
        logger.info("GROQ_API_KEY not set, AI features disabled")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/results_page")
def results_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={}
    )
