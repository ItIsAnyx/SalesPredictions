from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.auth.service import get_current_user

router = APIRouter()

# Используй пользователя, что по id искать
@router.get("")
def get_(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return