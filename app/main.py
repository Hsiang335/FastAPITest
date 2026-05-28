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

app = FastAPI()

#把 document API 掛進來。
app.include_router(document.router)

#把 user API 掛進來。
app.include_router(user.router)

# 建立資料表
Base.metadata.create_all(bind=engine)

 