from pydantic import BaseModel


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

    title: str

    content: str