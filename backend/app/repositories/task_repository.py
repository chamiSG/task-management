from __future__ import annotations

from datetime import UTC, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.models import TaskCreate, TaskResponse, TaskStatus, TaskUpdate


class TaskRepository:
    """
    Repository layer for task persistence using MongoDB (Motor).

    This class encapsulates all direct database access for tasks and should be
    used by a separate service layer or FastAPI dependencies.
    """

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str = "tasks") -> None:
        self._db: AsyncIOMotorDatabase = db
        self._collection: AsyncIOMotorCollection = db[collection_name]

    async def create_task(self, payload: TaskCreate) -> TaskResponse:
        """
        Insert a new task document and return the created task.
        """
        now = datetime.now(UTC)
        doc = {
            "_id": uuid4(),
            "title": payload.title,
            "description": payload.description,
            "status": payload.status,
            "owner_id": payload.owner_id,
            "created_at": now,
            "updated_at": now,
        }

        await self._collection.insert_one(doc)
        return TaskResponse(**doc)

    async def get_task_by_id(self, task_id: UUID) -> Optional[TaskResponse]:
        """
        Fetch a single task by its UUID identifier.
        """
        doc = await self._collection.find_one({"_id": task_id})
        if not doc:
            return None
        return TaskResponse(**doc)

    async def list_tasks(
        self,
        *,
        owner_id: Optional[UUID] = None,
        status: Optional[TaskStatus] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> List[TaskResponse]:
        """
        List tasks with optional filtering by owner and status.
        """
        query: dict = {}
        if owner_id is not None:
            query["owner_id"] = owner_id
        if status is not None:
            query["status"] = status

        cursor = (
            self._collection.find(query)
            .skip(max(skip, 0))
            .limit(max(limit, 1))
            .sort("created_at", 1)
        )

        results: List[TaskResponse] = []
        async for doc in cursor:
            results.append(TaskResponse(**doc))
        return results

    async def update_task(self, task_id: UUID, updates: TaskUpdate) -> Optional[TaskResponse]:
        """
        Apply partial updates to a task and return the updated document.
        """
        update_data = updates.model_dump(exclude_unset=True)

        # Remove keys explicitly set to None to avoid overwriting with nulls.
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            # Nothing to update; just return the current document.
            return await self.get_task_by_id(task_id)

        update_data["updated_at"] = datetime.now(UTC)

        doc = await self._collection.find_one_and_update(
            {"_id": task_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )

        if not doc:
            return None

        return TaskResponse(**doc)

    async def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a task by id. Returns True if a document was deleted.
        """
        result = await self._collection.delete_one({"_id": task_id})
        return result.deleted_count == 1

