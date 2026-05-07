from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class StoreItemDto(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StoreListDto(BaseModel):
    total_items: int
    page: int
    total_pages: int
    items: List[StoreItemDto]

class StoreCreateDto(BaseModel):
    store_name: str