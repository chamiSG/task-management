"""FastAPI application entry point and initialization."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app import __version__
from app.api.v1.router import api_router
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    from app.db.mongodb import MongoDBConnectionManager

    settings = get_settings()
    mongodb = MongoDBConnectionManager(settings)

    if settings.mongodb_url:
        await mongodb.connect()
        app.state.mongodb_client = mongodb.client
        app.state.mongodb_db = mongodb.database
    else:
        app.state.mongodb_client = None
        app.state.mongodb_db = None

    yield

    await mongodb.close()
    if hasattr(app.state, "mongodb_client"):
        app.state.mongodb_client = None
    if hasattr(app.state, "mongodb_db"):
        app.state.mongodb_db = None


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Production-ready tasks management API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
