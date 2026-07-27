from fastapi import APIRouter

from app.api.routes import analysis, results, health

router = APIRouter()

router.include_router(analysis.router, prefix="", tags=["analysis"])
router.include_router(results.router, prefix="", tags=["results"])
router.include_router(health.router, prefix="", tags=["health"])
