from sqlalchemy import select
from sqlalchemy.orm import Session

from models.task import TaskORM


class TaskRepository:
    """Ключевые операции с таблицей tasks в БД"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TaskORM]:
        """Получить все записи task"""
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str):
        """Получить запись task по id"""
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        """Создать запись task"""
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, TaskORM) -> None:
        """Удалить запись task"""
        self.db.delete(TaskORM)


# Метод scalars() в SQLAlchemy преобразует результат
# выполнения запроса так, чтобы вместо
# обычных строк (Row / кортежей) возвращать
# первый элемент из каждой строки в виде готовых ORM-объектов
# или скалярных значений.
