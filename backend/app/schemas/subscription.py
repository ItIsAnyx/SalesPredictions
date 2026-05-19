from pydantic import BaseModel, ConfigDict

class SubscriptionCreateDto(BaseModel):
    id: int
    duration_months: int

    model_config = ConfigDict(from_attributes=True)