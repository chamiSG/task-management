"""Health check endpoint."""

from fastapi import APIRouter, Depends

from app.dependencies import SettingsDep

router = APIRouter(tags=["health"])


@router.get("/health", status_code=200)
async def health_check(settings: SettingsDep) -> dict:
    """
    Health check endpoint for load balancers and monitoring.
    Returns application status and basic config (non-sensitive).
    """
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }
