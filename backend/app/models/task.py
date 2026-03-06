from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    owner_id: UUID


class TaskCreate(TaskBase):
    """
    Payload for creating a new task.

    _id, created_at and updated_at are set by the persistence layer.
    """

    pass


class TaskUpdate(BaseModel):
    """
    Payload for partially updating an existing task.

    All fields are optional; only provided values will be updated.
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    """
    Representation of a task returned from the API.
    """

    id: UUID = Field(alias="_id")
    title: str
    description: Optional[str] = None
    status: TaskStatus
    owner_id: UUID
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Task creation timestamp (UTC).",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last update timestamp (UTC).",
    )

    class Config:
        populate_by_name = True


class TaskListResponse(BaseModel):
    """
    Paginated list of tasks with total count.
    """

    items: List[TaskResponse]
    total: int
    limit: int
    skip: int
