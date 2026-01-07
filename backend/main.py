from fastapi import FastAPI
from config import settings
from dataset import load_dataset

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    df = load_dataset(backend_key)
    print(df)