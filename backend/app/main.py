import os
import pandas as pd
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.routers.auth import router as auth_router
from app.database.db import engine, Base
from app.database.populate import populate_db
from app.database.dataset import get_or_generate_dataset
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
