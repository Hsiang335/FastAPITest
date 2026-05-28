from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate
)
from app.services.security import get_current_user

router = APIRouter()


# ----------------------
# CREATE DOCUMENT
# ----------------------
@router.post(
    "/documents",
    response_model=DocumentResponse
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_document = Document(
        title=document.title,
        content=document.content,
        owner_id=current_user.id
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    return new_document

# ----------------------
# DELETE DOCUMENT
# ----------------------
@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 找文件
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    # 文件不存在
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # 檢查是不是本人文件
    if document.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    # 刪除
    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted"
    }


# ----------------------
# UPDATE DOCUMENT
# ----------------------
@router.put(
    "/documents/{document_id}",
    response_model=DocumentResponse
)
def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 找文件
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    # 文件不存在
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # 權限檢查
    if document.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    # 更新資料
    document.title = document_data.title

    document.content = document_data.content

    # 寫入 DB
    db.commit()

    # 更新 ORM 資料
    db.refresh(document)

    return document

# ----------------------
# GET MY DOCUMENTS
# ----------------------
@router.get(
    "/documents",
    response_model=List[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    documents = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).all()

    return documents