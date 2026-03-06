"""FastAPI application entry point and initialization."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app import __version__
from app.api.v1.router import api_router
from app.config import get_settings
from app.logging_config import configure_logging
from app.middleware import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    settings = get_settings()
    configure_logging(
        json_logs=not settings.debug,
        log_level="DEBUG" if settings.debug else "INFO",
    )

    from app.db.mongodb import MongoDBConnectionManager
    from app.repositories import TaskRepository

    mongodb = MongoDBConnectionManager(settings)

    if settings.mongodb_url:
        await mongodb.connect()
        app.state.mongodb_client = mongodb.client
        app.state.mongodb_db = mongodb.database

        if app.state.mongodb_db is not None:
            # Initialize indexes for the tasks collection to keep queries efficient.
            task_repository = TaskRepository(app.state.mongodb_db)
            await task_repository.init_indexes()
    else:
        app.state.mongodb_client = None
        app.state.mongodb_db = None

    yield

    await mongodb.close()
    if hasattr(app.state, "mongodb_client"):
        app.state.mongodb_client = None
    if hasattr(app.state, "mongodb_db"):
        app.state.mongodb_db = None


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Log unhandled exceptions with correlation ID and return a JSON 500."""
    log = structlog.get_logger(__name__)
    correlation_id = getattr(request.state, "correlation_id", None)
    structlog.contextvars.clear_contextvars()
    if correlation_id:
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    log.exception(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error_type=type(exc).__name__,
        error=str(exc),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


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

    app.add_exception_handler(Exception, global_exception_handler)
    app.add_middleware(RequestLoggingMiddleware)
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
