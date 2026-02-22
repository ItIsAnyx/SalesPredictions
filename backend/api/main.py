from fastapi import FastAPI
from config import settings
from dataset import load_dataset
from my_magazine.table import router as my_shop_router

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    df = load_dataset(backend_key)

    app.include_router(my_shop_router)
