from pydantic import BaseModel
from typing import Optional


class DocumentCreate(BaseModel):

    title: str

    content: str


class DocumentResponse(BaseModel):

    id: int

    title: str

    content: str

    owner_id: int

    class Config:
        from_attributes = True

class DocumentUpdate(BaseModel):

    title: Optional[str] = None

    content: Optional[str] = None

    class Config:
        from_attributes = True