"""Task management REST API endpoints."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import CurrentUserDep, DatabaseDep
from app.models import TaskCreate, TaskListResponse, TaskResponse, TaskStatus, TaskUpdate
from app.repositories import TaskRepository
from app.services import (
    InvalidStatusTransitionError,
    TaskNotFoundError,
    TaskService,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: DatabaseDep) -> TaskService:
    """
    FastAPI dependency that wires the MongoDB database into the task service.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not configured.",
        )

    repository = TaskRepository(db)
    return TaskService(repository)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    payload: TaskCreate,
    current_user: CurrentUserDep,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Create a new task.
    """
    try:
        return await service.create_task(payload)
    except InvalidStatusTransitionError as exc:
        # Unlikely during creation but kept for consistency.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=TaskListResponse,
    summary="List tasks",
)
async def list_tasks(
    owner_id: Optional[UUID] = None,
    status: Optional[TaskStatus] = None,
    limit: int = 50,
    skip: int = 0,
    service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    """
    List tasks with optional filters for owner and status.
    """
    return await service.list_tasks(
        owner_id=owner_id,
        status=status,
        limit=limit,
        skip=skip,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by id",
)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Retrieve a single task by its identifier.
    """
    try:
        return await service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
async def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    current_user: CurrentUserDep,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Update a task. Only provided fields will be modified.
    """
    try:
        return await service.update_task(task_id, payload)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
async def delete_task(
    task_id: UUID,
    current_user: CurrentUserDep,
    service: TaskService = Depends(get_task_service),
) -> None:
    """
    Delete a task by id.
    """
    try:
        await service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

