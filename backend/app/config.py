from pydantic_settings import BaseSettings
from pathlib import Path
from fastapi import HTTPException

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    APP_NAME: str = "SalesPrediction"
    APP_VERSION: str = "0.0.1"

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_PORT: int = 5432
    DB_DATABASE: str = "postgres"
    DB_HOST: str = "localhost"

    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "Lax"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config():
        env_file: str = ENV_PATH
        case_sensitive: bool = True

settings = Settings()

def validate_key(key: str):
    if key == settings.BACKEND_API_KEY:
        return True
    else:
        raise HTTPException(status_code=500, detail="Invalid API key")