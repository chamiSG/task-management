"""Audit log repository for persisting task audit entries."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.audit import AuditLogEntry


class AuditLogRepository:
    """
    Repository for writing audit log entries to MongoDB.
    """

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        collection_name: str = "audit_logs",
    ) -> None:
        self._collection = db[collection_name]

    async def insert_entry(
        self,
        *,
        action: str,
        task_id: UUID,
        user_id: str,
        timestamp: datetime | None = None,
    ) -> None:
        """
        Insert a single audit log entry.
        """
        entry = AuditLogEntry(
            action=action,
            task_id=task_id,
            user_id=user_id,
            timestamp=timestamp or datetime.now(UTC),
        )
        doc = entry.model_dump()  # Keep UUID and datetime for BSON
        await self._collection.insert_one(doc)
