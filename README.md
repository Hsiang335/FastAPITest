# FastAPITest
FastAPI 練習

## 安裝與環境

1. 建立並啟用虛擬環境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. 安裝專案依賴

```bash
pip install -r requirements.txt
```

3. 若要執行測試，安裝開發依賴

```bash
pip install -r requirements-dev.txt
```

## 執行方式

啟用虛擬環境後，啟動 FastAPI:

```bash
uvicorn app.main:app --reload
```

## 測試

執行 pytest：

```bash
source .venv/bin/activate
.venv/bin/python -m pytest -q
```

若要執行單一測試檔：

```bash
.venv/bin/python -m pytest app/test/test_user_service.py -q
```


【 瀏覽器 / 前端 Postman 】
                 │
                 │ 1. 發送 HTTP 請求 (例如: 註冊、登入)
                 ▼
     ┌─────────────────────────────────────────────────────────┐
     │                  Routers 層 (API 接口)                   │
     │  - post_register()  ───┐                                 │
     │  - post_login()     ───┼──────────────────────────────┐  │
     └────────────────────────┼──────────────────────────────┼──┘
                              │                              │
                              │ 2. 透過 Depends() 請求依賴    │
                              ▼                              │
     ┌──────────────────────────────────────────────────┐    │
     │             core/deps.py (工廠中心)               │    │
     │                                                  │    │
     │   get_user_service() ─── 檢查 settings.env       │    │
     │                                                  │    │
     │         ├── if "testing"     ──> 注入 FakeRepo   │    │
     │         └── else (prod/dev)  ──> 注入 RealRepo   │    │
     └────────────────────────┬─────────────────────────┘    │
                              │                              │
                              │ 3. 產出帶有對應 Repo          │
                              │    的 UserService 物件        │
                              ▼                              ▼
     ┌─────────────────────────────────────────────────────────┐
     │                Services 層 (UserService)                │
     │                                                         │
     │  - register_user(db, username, password)                │
     │  - authenticate(db, username, password)                 │
     └────────────────────────┬────────────────────────────────┘
                              │
                              │ 4. 根據環境呼叫對應的儲存庫
                              ▼
     ┌─────────────────────────────────────────────────────────┐
     │                 Repositories 層 (資料庫操作)             │
     │                                                         │
     │   [ 測試環境 testing ]         [ 生產環境 production ]   │
     │     FakeUserRepo                  UserRepository        │
     │     (記憶體模擬, 秒回)               (連線真實 PostgreSQL)│
     └─────────────────────────────────────────┬───────────────┘
                                               │
                                               │ 5. 寫入實體資料
                                               ▼
                                     💾 【 PostgreSQL DB 】