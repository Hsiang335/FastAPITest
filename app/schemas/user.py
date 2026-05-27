from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str = Field(max_length=72)

    class Config:
        from_attributes = True

# app/schemas/user.py

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True