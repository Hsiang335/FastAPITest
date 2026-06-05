from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService
from app.core.deps import get_user_service
from app.core.security import create_access_token


router = APIRouter(tags=["Auth"])


# ----------------------
# REGISTER
# ----------------------
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.register_user(
        db,
        user.username,
        user.password
    )

# ----------------------
# LOGIN
# ----------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):

    user = service.authenticate(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "login success",
        "user": user.username
    }


