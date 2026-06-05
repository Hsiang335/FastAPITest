專案名稱：FastAPITest

簡短說明

這是作者的第一個 FastAPI 練習專案，示範使用 FastAPI + SQLAlchemy + JWT + Docker + PostgreSQL 的基本全端後端能力，包含使用者註冊/登入（JWT）以及文件（Document）的 CRUD。

目標讀者

- 面試官：快速理解專案架構、設計決策與重點實作
- 自我練習：用來複習程式流程與準備面試回答

專案總覽（高階架構）

- `app/`：應用程式主程式碼
  - `main.py`：FastAPI 應用啟動點（`uvicorn app.main:app --reload`）
  - `core/`：核心設定與共用邏輯
    - `config.py`：環境與設定（使用 pydantic-settings）
    - `deps.py`：FastAPI 依賴注入工廠（如 `get_user_service()`）
    - `security.py`：JWT、密碼雜湊與授權相關邏輯
  - `database/`：DB 連線與 Session 管理（`connection.py`）
  - `models/`：SQLAlchemy ORM model（`user.py`, `document.py`）
  - `repositories/`：資料存取層（Repository pattern）
    - `user_repo.py`：User 的 DB 操作（create, get_by_username）
    - `fake_repo.py`：測試用的假實作（用於 testing env）
  - `schemas/`：Pydantic 請求/回應模型（DTO）
  - `services/`：商業邏輯層（Service）
    - `user_service.py`：使用者註冊/驗證邏輯（使用 repo）
  - `routers/`：API 路由（Auth、Documents）
  - `test/`：單元測試（pytest）

主要設計決策與分層理由（系統性說明）

- 分層：Router -> Service -> Repository -> Database
  - Router (HTTP 層)：負責驗證 request、權限、返回 response。
  - Service (商業邏輯)：負責核心流程（例如 hash password、呼叫 repo、處理回傳），對外呈現較抽象的方法，例如 `register_user()`、`authenticate()`。
  - Repository (資料層)：與 ORM/DB 互動，負責建立 ORM 實例並 commit。把 ORM 細節封裝，讓 service 易於被替換/測試（可注入 fake repo）。
  - Database：管理 Session/engine，集中 DB 連線設定。

- 為何把 `User` 的建立移到 repository？
  - 讓 service 不需要 import ORM model（減少測試時的依賴），也更符合單一職責，測試時可使用 `FakeUserRepo` 避免初始化整個 ORM 映射。

資料流程（以註冊/登入與文件 CRUD 為例，簡要說明）

1. 註冊（Register）
   - `POST /register` -> Router 接收 `UserCreate` schema
   - Router 透過 DI `get_user_service()` 取得 `UserService`
   - `UserService.register_user(db, username, password)`
     - password 被 `hash_password()` 處理
     - 呼叫 `repo.create(db, username, hashed)`（Repository 建立 ORM instance、commit、refresh）
   - 回傳新建立的 user（或其部分欄位）

2. 登入（Login）
   - `POST /login` -> Router 使用 `OAuth2PasswordRequestForm` 接收憑證
   - `UserService.authenticate(db, username, password)`
     - `repo.get_by_username(db, username)` 取得 user
     - `verify_password()` 驗證密碼
     - 若成功則產生 JWT（在 `security.py` 中）並回傳 token

3. 文件（Document）CRUD
   - Router 管理 `GET /documents`（分頁、搜尋）、`POST /documents`（建立）、`PUT /documents/{id}`（更新）、`DELETE /documents/{id}`（刪除）
   - 更新路由支援 partial update（schema 欄位可為 Optional，router 只在提供欄位時覆寫）

環境與測試

- 設定由 `app/core/config.py` 管理（使用 pydantic-settings）：`database_url`、`secret_key`、`algorithm`、`access_token_expire_minutes`、`env`（production|development|testing）
- `app/core/deps.py` 根據 `settings.env` 在 `testing` 環境動態注入 `FakeUserRepo`，提高測試隔離性
- `conftest.py`（測試）會設定測試時需要的環境變數（例如使用 sqlite in-memory）
- 使用 `pytest` 作為測試框架（`requirements-dev.txt` 已包含 pytest）

部署/執行

- 開發：
  ```bash
  source .venv/bin/activate
  uvicorn app.main:app --reload
  ```
- Docker / Production（專案已有 Dockerfile 與 docker-compose 可進一步擴充）

面試說明重點（口語化練習句）

- 開場一句話介紹："這個專案是我用 FastAPI 實作的練習專案，功能包含使用者註冊/登入（JWT）、文件的 CRUD，以及環境設定與測試。"
- 架構介紹："我採用分層設計：Router 處理 HTTP，Service 處理商業邏輯，Repository 封裝資料存取，Database 管理連線。"
- 測試與可替換性："為了讓 service 可測試，我把資料建立交給 repository，並實作 `FakeUserRepo` 以便在 testing 環境注入替代實作，避免初始化整個 SQLAlchemy 映射。"
- 權責清楚："`security.py` 處理 token 與密碼雜湊，`config.py` 用 pydantic-settings 管理環境設定，這樣不同環境（dev/test/prod）可有不同行為。"
- 優化與未來改進："若要擴充，我會加入 repository interface、更多單元與整合測試、CI/CD 與更完善的錯誤/日誌系統。"

常見面試問題 & 建議回答要點

- Q: 為什麼要把建立 ORM 實例放到 repository？
  - A: 使 service 不需直接依賴 ORM 型別，減少測試耦合，並把 DB 行為封裝在一層。
- Q: 如何保護密碼與 token？
  - A: 使用 `passlib`/bcrypt 做雜湊並儲存 hash；用 JWT 封裝 user identity，設定合理過期時間並用 `SECRET_KEY` 簽名。
- Q: 如果要添加 RBAC（Role-Based Access Control）你會怎麼做？
  - A: 在 `security.py` 加上 decode token 後檢查角色，Router 加上依賴條件，或用 middleware 在 request 階段處理。

練習題（自我檢測）

- 用 2 分鐘口頭描述此專案架構（練習用）
- 實作：新增 `PATCH /documents/{id}`，只更新提供的欄位（你已支援）
- 實作：新增 `tests` 檔案，覆蓋 document 的 CRUD 行為

參考檔案

- 專案啟動點：[app/main.py](app/main.py)
- 設定：[app/core/config.py](app/core/config.py)
- 依賴注入：[app/core/deps.py](app/core/deps.py)
- 路由（Auth）：[app/routers/user_router.py](app/routers/user_router.py)
- 路由（Documents）：[app/routers/document_router.py](app/routers/document_router.py)
- Service 範例：[app/services/user_service.py](app/services/user_service.py)
- Repository 範例：[app/repositories/user_repo.py](app/repositories/user_repo.py)
- Fake repo（測試）：[app/repositories/fake_repo.py](app/repositories/fake_repo.py)
- 測試：`app/test/test_user_service.py`、`app/services/test_service.py`

---

如果你想，我可以把上面內容精簡成一頁面試講稿（逐段要講的要點與一句話開場），或生成一個 2 分鐘自我介紹稿幫你練習口頭說明。