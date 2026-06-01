import os
from dotenv import load_dotenv

# 尋找 .env
# 讀取內容
# 載入到環境變數
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in .env")
