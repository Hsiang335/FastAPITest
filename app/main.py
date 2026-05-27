from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.routers import user
from app.database.connection import engine
from app.models.base import Base
from app.models import user as user_model


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

#把 user API 掛進來。
app.include_router(user.router)

# 建立資料表
Base.metadata.create_all(bind=engine)


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.get("/")
# def root():
#     return {"message": "FastAPI Portfolio Project"}

# @app.get("/items/")
# async def read_items(q: str | None = Query(default=None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}


