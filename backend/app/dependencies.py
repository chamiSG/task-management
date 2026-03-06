"""Dependency injection definitions."""

from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import Settings, get_settings
from app.db.mongodb import get_database

# Re-export for convenience
__all__ = ["get_settings", "SettingsDep", "get_database", "DatabaseDep"]


SettingsDep = Annotated[Settings, Depends(get_settings)]
DatabaseDep = Annotated[AsyncIOMotorDatabase | None, Depends(get_database)]
