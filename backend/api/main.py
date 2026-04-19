import pandas as pd
from fastapi import FastAPI
from config import settings, validate_key
from dataset import get_or_generate_dataset

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    # Здесь будет условие проверки существования БД. Если БД уже есть, и она заполнена, то загрузка датасета скипнется

    df = get_or_generate_dataset("retail_forecasting_dataset.csv")
    app.state.dataset = df
    print("Датасет успешно загружен в приложение.")
    print(f"Размер датасета: {df.shape}")
    print(df.head())