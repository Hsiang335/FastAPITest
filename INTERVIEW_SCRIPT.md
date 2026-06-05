# FastAPITest 面試講稿

## 一句話開場

「這是一個我自己的 FastAPI 練習專案，主要示範後端分層架構、JWT 登入驗證、資料庫存取、測試與環境配置。」

## 主要講稿段落

### 1. 專案目的與技術選擇

- 目的：建立一個簡單但可擴充的後端範例，練習 FastAPI、SQLAlchemy、JWT、Docker、PostgreSQL。
- 技術：FastAPI 做 API server、SQLAlchemy 處理 ORM、Pydantic 做資料驗證、JWT 做登入 token、pytest 做單元測試。
- 這個專案適合展示我對後端分層設計與測試思考的能力。

### 2. 架構分層說明

- `app/main.py`：API 入口，啟動 FastAPI 應用。
- `app/core/`：共用設定與依賴注入。
  - `config.py`：環境設定，支援 production / development / testing。
  - `deps.py`：依賴提供者，像是 `get_user_service()`。
  - `security.py`：密碼雜湊、JWT 產生與驗證。
- `app/database/`：DB 連線與 Session 管理。
- `app/models/`：ORM entity 定義。
- `app/repositories/`：資料存取層，封裝 DB 操作。
- `app/services/`：商業邏輯層，處理註冊、登入與認證流程。
- `app/routers/`：API 路由層，對應 endpoint 與 request/response。
- `app/test/`：測試程式碼，驗證 service 行為。

### 3. 主要功能流程

- 註冊：`POST /register` -> 資料驗證 -> password hash -> repository 建 user -> commit。
- 登入：`POST /login` -> 取 user -> 驗證密碼 -> 回傳 JWT。
- Document CRUD：`GET /documents`, `POST /documents`, `PUT /documents/{id}`, `DELETE /documents/{id}`。
- 更新支援部分欄位，只要有提供就更新，沒提供就保留。

### 4. 設計重點

- 分層架構讓每個模組只負責一件事。
- Service 不直接處理 DB 細節，Repository 封裝 ORM 操作。
- 測試環境透過 `FakeUserRepo` 注入，避免真實 ORM 依賴，測試更輕量。
- 使用 `pydantic-settings` 管理環境變數，提高設定一致性。

### 5. 面試常見問答要點

- 為什麼分層？
  - 「這樣可降低耦合、提高可維護性，Router 專注 HTTP，Service 專注邏輯，Repository 專注資料存取。」
- 為什麼要用 Repository？
  - 「讓 DB 存取集中，便於替換實作與測試，比如注入 `FakeUserRepo`。」
- JWT 怎麼保護？
  - 「密碼用 bcrypt 雜湊，JWT 用 `SECRET_KEY` 簽名並設定過期時間，避免明碼儲存與長期有效 token。」
- 測試怎麼做？
  - 「使用 pytest，測試依賴由 `conftest.py` 設定環境變數，測試時用 in-memory DB 參數和 fake repo。」

## 2 分鐘自我介紹稿

### 開場（約 20 秒）

"這個專案是我第一個 FastAPI 練習專案，我想展示自己的後端設計能力。專案主要實作使用者註冊/登入、JWT 認證和文件 CRUD，並且加入了測試與環境配置。"

### 架構說明（約 40 秒）

"架構方面我採用清楚的分層：`routers` 負責 API；`services` 負責商業邏輯；`repositories` 負責資料存取；`core` 包含設定與安全；`database` 管理 DB 連線。這樣做的好處是各層責任分明、可維護性高。"

### 功能與重點（約 40 秒）

"功能上我實作註冊、登入和文件 CRUD。註冊時會先把密碼用 bcrypt 雜湊再儲存；登入會驗證密碼並回傳 JWT。文件更新支援部分欄位更新，避免覆寫未提供的內容。測試方面，我有用 pytest 以及 `FakeUserRepo` 來降低測試耦合。"

### 收尾與未來方向（約 20 秒）

"這個專案讓我熟悉 FastAPI 的分層設計、JWT 安全、SQLAlchemy ORM 和測試流程。未來我打算繼續擴充權限控制、資料驗證與整合測試，並把它包成更完整的 API 服務。"
