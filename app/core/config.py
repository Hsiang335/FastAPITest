from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # environment: production | development | testing
    env: Literal["production", "development", "testing"] = "production"

    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()