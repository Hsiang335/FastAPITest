from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate

from app.services.security import hash_password

from typing import List
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        #password=user.password
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User created"
    }

