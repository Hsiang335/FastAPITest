from enum import Enum

from fastapi import FastAPI
from app.routers import user
from app.database.connection import engine
from app.routers import document
from app.database.connection import Base

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

#把 document API 掛進來。
app.include_router(document.router)

#把 user API 掛進來。
app.include_router(user.router)

# 建立資料表
Base.metadata.create_all(bind=engine)

 