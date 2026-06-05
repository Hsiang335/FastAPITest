import sys
import os

# Ensure project root is on sys.path so `import app` works during tests
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Provide default settings for tests so pydantic Settings() can initialize
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "testsecret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
# set env to 'testing' so deps.py uses FakeUserRepo
os.environ.setdefault("ENV", "testing")
