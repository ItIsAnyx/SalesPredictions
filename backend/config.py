import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SalesPrediction"
    APP_VERSION: str = "0.0.1"

    BACKEND_API_KEY: str

    class Config():
        env_file: str = ".env"
        case_sensitive: bool = True

settings = Settings()