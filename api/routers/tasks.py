from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_task_service
from schemas.task import CreateTaskSchema, TaskSchema, UpdateTaskSchema
from services.task import TaskNotFound, TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def get_tasks(service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:

    return service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: CreateTaskSchema, service: TaskService = Depends(get_task_service)
) -> TaskSchema:

    return service.create_task(payload)


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: UpdateTaskSchema,
    service: TaskService = Depends(get_task_service),
) -> TaskSchema:

    try:
        return service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, service: TaskService = Depends(get_task_service)) -> None:

    try:
        return service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )
