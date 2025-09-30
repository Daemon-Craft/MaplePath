from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MaplePath API"

    # Database
    DATABASE_URL: str
    DATABASE_URL_PROD: Optional[str] = None

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()
