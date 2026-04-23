import pandas as pd
from fastapi import FastAPI
from config import settings, validate_key
from dataset import get_or_generate_dataset
from database.tables import Base
from database.db import engine

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    init_db()

    df = get_or_generate_dataset("retail_forecasting_dataset.csv")
    app.state.dataset = df # Временно, чтоб датасет было видно в памяти приложения
    print("Датасет успешно загружен в приложение.")
    print(f"Размер датасета: {df.shape}")
    print(df.head())


def init_db():
    Base.metadata.create_all(bind=engine)
    print("БД инициализирована")