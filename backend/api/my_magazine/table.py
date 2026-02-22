from config import verify_key
from fastapi import APIRouter
from pydantic import BaseModel

class ShopTitle(BaseModel):
    title: str

router = APIRouter()

@router.get("/api/my_shop/title", response_model=ShopTitle)
async def get_shop_name(shop_id: int, backend_key):
    verify_key(backend_key)
    return {"title": "Nishtyak"}

@router.post("/api/my_shop/title", response_model=ShopTitle)
async def get_shop_name(payload: ShopTitle, shop_id: int, backend_key):
    verify_key(backend_key)
    return {"title": payload.title}