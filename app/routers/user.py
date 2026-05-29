from typing import List
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password
)
from fastapi import APIRouter, Depends, HTTPException
# 修正重點：這裡必須記得引入 OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Auth"]
)

# 宣告 OAuth2 規範，告訴 Swagger 你的登入 API 路徑是 "login"
# 注意：這裡對應的是 @router.post("/login") 的相對路徑
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ----------------------
# GET ME (獲取當前登入用戶)
# ----------------------
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "username": current_user.username
    }

# ----------------------
# LOGIN (登入換取 Token)
# ----------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    使用 OAuth2PasswordRequestForm 接收來自大鎖或表單的資料：
    欄位固定為 form_data.username 與 form_data.password
    """
    db_user = (
        db.query(User).filter(User.username == form_data.username).first()
    )

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 簽發 Token
    token = create_access_token(data={"sub": db_user.username})

    # 回傳標準規範格式，Swagger 大鎖才會自動讀取成功
    return {"access_token": token, "token_type": "bearer"}

# ----------------------
# GET USERS (獲取所有用戶)
# ----------------------
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ----------------------
# REGISTER (註冊新用戶)
# ----------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}