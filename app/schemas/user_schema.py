from pydantic import BaseModel, field_validator


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long")
        return v


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}