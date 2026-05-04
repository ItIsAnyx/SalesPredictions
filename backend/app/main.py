import os
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.routers.auth import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(auth_router, prefix="/api/auth")

if __name__ == "__main__":
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
# Загрузка всех ключей
# backend_key = settings.BACKEND_API_KEY

# @app.on_event("startup")
# async def Start():
#     init_db()

#     df = get_or_generate_dataset("retail_forecasting_dataset.csv")
#     app.state.dataset = df # Временно, чтоб датасет было видно в памяти приложения
#     print("Датасет успешно загружен в приложение.")
#     print(f"Размер датасета: {df.shape}")
#     print(df.head())


# def init_db():
#     Base.metadata.create_all(bind=engine)
#     print("БД инициализирована")