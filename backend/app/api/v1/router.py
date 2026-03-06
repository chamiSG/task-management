"""API v1 router - aggregates all v1 route modules."""

from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()

api_router.include_router(health.router)
