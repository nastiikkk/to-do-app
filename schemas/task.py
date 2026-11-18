from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # чтобы model validate мог использовать аттрибуты

    id: str
    title: str
    completed: bool = False


class CreateTaskSchema(BaseModel):
    title: str


class UpdateTaskSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
