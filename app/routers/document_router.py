from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document_schema import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate
)
from app.core.security import get_current_user

router = APIRouter(
    tags=["Documents"]
)

# ----------------------
# GET MY DOCUMENTS
# Pagination + Search
# ----------------------
@router.get(
    "/documents",
    response_model=List[DocumentResponse],
    summary="Get Documents",
    description="Get current user's documents with pagination and search"
)
def get_documents(
    page: int = 1,
    limit: int = 5,
    keyword: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Document).filter(
        Document.owner_id == current_user.id
    )

    # Search
    if keyword:

        query = query.filter(
            Document.title.ilike(f"%{keyword}%")
        )

    # Pagination
    skip = (page - 1) * limit

    documents = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return documents

@router.post(
    "/documents",
    response_model=DocumentResponse,
    summary="Create Document",
    description="Create a new document for current user",
   
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
@router.delete(
    "/documents/{document_id}",
    summary="Delete Document",
    description="Delete current user's document"
)
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
    response_model=DocumentResponse,
    summary="Update Document",
    description="Update current user's document"
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

    # 更新資料（僅在有提供時才覆寫，支援部分更新）
    if document_data.title is not None:
        document.title = document_data.title

    if document_data.content is not None:
        document.content = document_data.content

    # 寫入 DB
    db.commit()

    # 更新 ORM 資料
    db.refresh(document)

    return document


