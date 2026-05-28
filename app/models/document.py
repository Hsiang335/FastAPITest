from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    content = Column(String)

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship("User")