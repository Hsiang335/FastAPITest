from enum import Enum

from fastapi import FastAPI
from app.routers import user_router
from app.routers import document_router

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI(

    title="FastAPI Portfolio Project",

    description="""
A production-style FastAPI backend project.

Features:
- JWT Authentication
- User System
- Documents CRUD
- Pagination & Search
- PostgreSQL
- SQLAlchemy ORM
"""
)

app.include_router(document_router.router)
app.include_router(user_router.router)