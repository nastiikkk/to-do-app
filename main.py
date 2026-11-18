from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from core.config import allow_origin
from db.session import engine
from models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origin,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.include_router(api_router)
    return app


app = create_app()

# class CategoryORM:
#     ...

# class CreateCategory(BaseModel):
#     name: str


# class UpdateCategory(BaseModel):
#     name: str | None = None

# categories: list[CategoryORM] = []

# @app.get("/categories")
# def get_categories():
#     return categories


# @app.post("/categories", status_code=status.HTTP_201_CREATED)
# def create_category(payload: CreateCategory):
#     new_category = CategoryORM(id=str(uuid4()), name=payload.name)
#     categories.append(new_category)
#     return new_category


# @app.patch("/categories/{id}")
# def update_category(id: str, payload: UpdateCategory):
#     for category in categories:
#         if category.id == id:
#             if payload.name is not None:
#                 category.name = payload.name
#             return category
#     raise HTTPException(status_code=404, detail= "Category not found")


# @app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(id: str):
#     for category in categories:
#         if category.id == id:
#             categories.remove(category)
#             found_category = True
#             break
#     else:
#         raise HTTPException(status_code=404, detail= "Category not found")
