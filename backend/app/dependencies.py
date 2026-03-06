"""Dependency injection definitions."""

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings

# Re-export for convenience
__all__ = ["get_settings", "SettingsDep"]


SettingsDep = Annotated[Settings, Depends(get_settings)]
