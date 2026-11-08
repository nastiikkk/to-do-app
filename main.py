from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker[Session](bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)





class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool 


class CreateTaskSchema(BaseModel):
    title: str


class UpdateTaskSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)
    

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()

    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTaskSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    return task_orm_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: UpdateTaskSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_to_update = db.get(TaskORM, task_id)
    if task_to_update is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title is not None:
        task_to_update.title = payload.title
    if payload.completed is not None:
        task_to_update.completed = payload.completed
    db.commit()
    return task_to_update

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task_to_delete = db.get(TaskORM, task_id)
    db.delete(task_to_delete)
    db.commit()



class CategoryORM(BaseModel):
    id: str
    name: str


class CreateCategory(BaseModel):
    name: str


class UpdateCategory(BaseModel):
    name: str | None = None

categories: list[CategoryORM] = []

@app.get("/categories")
def get_categories():
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CreateCategory):
    new_category = CategoryORM(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category


@app.patch("/categories/{id}")
def update_category(id: str, payload: UpdateCategory):
    for category in categories:
        if category.id == id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=404, detail= "Category not found")


@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str):
    for category in categories:
        if category.id == id:
            categories.remove(category)
            found_category = True
            break
    else:
        raise HTTPException(status_code=404, detail= "Category not found")