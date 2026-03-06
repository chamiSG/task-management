"""API v1 router - aggregates all v1 route modules."""

from fastapi import APIRouter

from app.api.v1 import health, tasks

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(tasks.router)
