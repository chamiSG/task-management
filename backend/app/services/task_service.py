from __future__ import annotations

from typing import Iterable, Optional
from uuid import UUID

from app.models import TaskCreate, TaskListResponse, TaskResponse, TaskStatus, TaskUpdate
from app.repositories import TaskRepository


class TaskNotFoundError(Exception):
    """Raised when a task with the given id does not exist."""


class InvalidStatusTransitionError(Exception):
    """Raised when attempting an invalid task status transition."""


class TaskService:
    """
    Application service for task-related business logic.

    This layer coordinates validation, status transitions, and repository usage.
    It should contain no transport / HTTP-specific concerns.
    """

    # Allowed status transitions for business rules:
    # - todo -> in_progress
    # - in_progress -> done
    # Once a task is done, its status cannot change further.
    _ALLOWED_STATUS_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
        TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
        TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
        TaskStatus.DONE: set(),
    }

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def create_task(self, payload: TaskCreate) -> TaskResponse:
        """
        Apply business validation and create a new task.
        """
        # Example place for additional domain validation (e.g., quotas per owner).
        return await self._repository.create_task(payload)

    async def get_task(self, task_id: UUID) -> TaskResponse:
        """
        Return a single task or raise if not found.
        """
        task = await self._repository.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found.")
        return task

    async def list_tasks(
        self,
        *,
        owner_id: Optional[UUID] = None,
        status: Optional[TaskStatus] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> TaskListResponse:
        """
        List tasks with optional filters, returning a paginated response with
        total count.
        """
        items, total = await self._repository.list_tasks(
            owner_id=owner_id,
            status=status,
            limit=limit,
            skip=skip,
        )
        return TaskListResponse(items=items, total=total, limit=limit, skip=skip)

    async def update_task(self, task_id: UUID, updates: TaskUpdate) -> TaskResponse:
        """
        Update a task with business validation and status transition rules.
        """
        # Load current state for validation.
        current = await self._repository.get_task_by_id(task_id)
        if current is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found.")

        # Enforce status transition rules when a new status is provided.
        if updates.status is not None:
            self._validate_status_transition(current.status, updates.status)

        updated = await self._repository.update_task(task_id, updates)
        if updated is None:
            # The task may have been deleted between read and update.
            raise TaskNotFoundError(f"Task with id {task_id} not found.")

        return updated

    async def delete_task(self, task_id: UUID) -> None:
        """
        Delete a task, raising if it does not exist.
        """
        deleted = await self._repository.delete_task(task_id)
        if not deleted:
            raise TaskNotFoundError(f"Task with id {task_id} not found.")

    def _validate_status_transition(
        self,
        current_status: TaskStatus,
        new_status: TaskStatus,
    ) -> None:
        """
        Ensure that the requested status change is allowed by business rules.
        """
        if current_status == new_status:
            return

        allowed: Iterable[TaskStatus] = self._ALLOWED_STATUS_TRANSITIONS.get(
            current_status, set()
        )
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                f"Cannot change status from {current_status.value!r} "
                f"to {new_status.value!r}."
            )

