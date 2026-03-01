from fastapi import FastAPI
from config import settings
from dataset import load_dataset, dataset_preprocessing

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

# Загрузка всех ключей
backend_key = settings.BACKEND_API_KEY

@app.on_event("startup")
async def Start():
    # Здесь будет условие проверки существования БД. Если БД уже есть, и она заполнена, то загрузка датасета скипнется
    df = load_dataset(backend_key)
    df = dataset_preprocessing(df)