import os
import pandas as pd
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.routers.auth import router as auth_router
from database.db import engine, Base
from database.populate import populate_db
from dataset import get_or_generate_dataset

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(auth_router, prefix="/api/auth")

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

if __name__ == "__main__":
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)