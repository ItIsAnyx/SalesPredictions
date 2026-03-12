from fastapi import FastAPI
from config import settings
from dataset import gen_date_conditions

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    # Здесь будет условие проверки существования БД. Если БД уже есть, и она заполнена, то загрузка датасета скипнется
    df = gen_date_conditions(backend_key, "2024-01-01", "2026-01-01")
    print(df)