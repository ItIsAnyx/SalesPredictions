from pydantic_settings import BaseSettings
from fastapi import HTTPException

class Settings(BaseSettings):
    APP_NAME: str = "SalesPrediction"
    APP_VERSION: str = "0.0.1"

    BACKEND_API_KEY: str

    class Config:
        env_file: str = ".env"
        case_sensitive: bool = True

settings = Settings()

def verify_key(key):
    if key != settings.BACKEND_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid backend key")