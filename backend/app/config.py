"""Application configuration and environment variable management."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Tasks Management API", description="Application name")
    debug: bool = Field(default=False, description="Enable debug mode")
    environment: str = Field(default="development", description="Environment name")

    # Server
    host: str = Field(default="0.0.0.0", description="Server bind host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")

    # API
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 URL prefix")

    # Auth / JWT
    jwt_secret_key: str = Field(
        default="change-me-in-production-please-change-me",
        min_length=32,
        description="Secret key for signing JWT tokens",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm",
    )
    access_token_expires_minutes: int = Field(
        default=60,
        ge=1,
        le=60 * 24 * 7,
        description="Access token lifetime in minutes",
    )

    # Demo user credentials (for development only)
    demo_username: str = Field(
        default="admin",
        description="Demo username for simple authentication.",
    )
    demo_password: str = Field(
        default="admin",
        description="Demo plaintext password for simple authentication.",
    )

    # MongoDB (Motor)
    mongodb_url: Optional[str] = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URL",
    )
    mongodb_database_name: str = Field(
        default="tasks_management",
        description="Default database name",
    )
    mongodb_min_pool_size: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Minimum connections in the pool",
    )
    mongodb_max_pool_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum connections in the pool",
    )
    mongodb_max_idle_time_ms: int = Field(
        default=30000,
        ge=0,
        description="Max idle time for a connection in the pool (ms)",
    )
    mongodb_server_selection_timeout_ms: int = Field(
        default=5000,
        ge=0,
        description="Timeout for server selection (ms)",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance (singleton per process)."""
    return Settings()
