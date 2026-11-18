from sqlalchemy.orm import Session

from repositories.task import TaskRepository
from schemas.task import CreateTaskSchema, TaskSchema, UpdateTaskSchema


class TaskNotFound(Exception):
    pass


class TaskService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.task_repository.get_all()
        return [TaskSchema.model_validate(task_orm) for task_orm in tasks]

    def create_task(self, payload: CreateTaskSchema) -> TaskSchema:
        task = self.task_repository.create(payload.title)
        self.db.commit()
        self.db.refresh(task)
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, payload: UpdateTaskSchema) -> TaskSchema:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFound

        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed

        self.db.commit()
        self.db.refresh(task)

        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFound

        self.task_repository.delete(task)

        self.db.commit()
