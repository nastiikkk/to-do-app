from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class TaskORM(BaseModel):
    id: str
    title: str
    completed: bool 


class CreateTask(BaseModel):
    title: str


class UpdateTask(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks: list[TaskORM] = []

@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask):
    new_task = TaskORM(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: UpdateTask):
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            break



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