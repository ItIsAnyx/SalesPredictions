from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductPriceUpdateDto(BaseModel):
    price: int
    region_id: int
    season: str
    weather_condition: str
    weekend: bool

class ProductCreateDto(BaseModel):
    title: str
    store_id: int
    category_id: int

    price: Optional[float] = None
    region_id: Optional[int] = None
    season: Optional[str] = None
    weather_condition: Optional[str] = None
    weekend: Optional[bool] = None

class ProductInfoDto(BaseModel):
    id: int
    title: str