# app/services/user_service.py

from app.core.security import hash_password, verify_password
# 修正 1：刪除了未使用的 User 模型引入
# 修正 2：刪除了未使用的 UserRepository 引入（因為是用注入的，不需要在檔案頭引入具體實作）

class UserService:

    def __init__(self, repo):
        """
        透過建構子注入不特定的 Repository，提高可測試性
        """
        self.repo = repo

    def register_user(self, db, username: str, password: str):
        """
        註冊使用者：負責將明文密碼加密，再交由 repo 存入資料庫
        """
        # 安全核心：絕對不在資料庫存明文密碼
        hashed = hash_password(password)
        
        # 呼叫儲存庫寫入資料庫
        return self.repo.create(db, username=username, password=hashed)

    def authenticate(self, db, username: str, password: str):
        """
        使用者驗證（登入）：比對帳號是否存在、密碼是否正確
        """
        user = self.repo.get_by_username(db, username)

        # 安全防禦 1：若找不到使用者，立刻返回 None
        if not user:
            return None

        # 安全防禦 2：使用 passlib 安全地驗證「明文密碼」與「資料庫的雜湊密碼」是否相符
        if not verify_password(password, user.password):
            return None

        # 雙重驗證通過，回傳使用者物件
        return user