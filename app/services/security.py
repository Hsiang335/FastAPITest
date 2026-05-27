from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta,timezone
 

from jose import jwt, JWTError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.database.connection import get_db
from app.models.user import User
from sqlalchemy.orm import Session



SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token"
        )

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

# 密碼 hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# JWT 設定
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# hash 密碼
def hash_password(password: str):
    return pwd_context.hash(password)

# 驗證密碼
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 建立 token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)