"""Audit log model for task create/update events."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AuditLogEntry(BaseModel):
    """
    A single audit log entry for task-related actions.
    Stored in the audit_logs collection.
    """

    action: str = Field(description="Action performed, e.g. 'created', 'updated'")
    task_id: UUID = Field(description="ID of the task")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the action occurred (UTC).",
    )
    user_id: str = Field(description="Identifier of the user who performed the action")
