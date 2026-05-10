from pydantic import BaseModel, Field

class RegionPayload(BaseModel):
    title: str = Field(min_length=1, max_length=64)