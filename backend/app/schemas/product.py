from pydantic import BaseModel
from typing import Optional


class ProductPriceUpdateDto(BaseModel):
    price: float
    region_id: int
    weather_condition: str

class ProductCreateDto(BaseModel):
    title: str
    store_id: int
    category_id: int

    price: Optional[float] = None
    region_id: Optional[int] = None
    weather_condition: Optional[str] = None

class ProductInfoDto(BaseModel):
    id: int
    title: str