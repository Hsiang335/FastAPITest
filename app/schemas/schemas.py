from pydantic import BaseModel


# 建立用（Request）
class UserCreate(BaseModel):
    name: str
    email: str


# 回傳用（Response）
class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
