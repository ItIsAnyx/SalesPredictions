import pandas as pd
from fastapi import FastAPI
from config import settings, validate_key
from dataset import get_or_generate_dataset
from database.tables import Base
from database.db import engine
from database.populate import populate_db

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    init_db()

    df = get_or_generate_dataset("retail_forecasting_dataset.csv")
    print(f"Размер датасета: {df.shape}")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Weekend"] = df["Weekend"].astype(bool)

    populate_db(df)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("БД инициализирована")