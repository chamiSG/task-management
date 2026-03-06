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

    # Optional: Database (placeholder for future use)
    database_url: Optional[str] = Field(default=None, description="Database connection URL")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance (singleton per process)."""
    return Settings()
