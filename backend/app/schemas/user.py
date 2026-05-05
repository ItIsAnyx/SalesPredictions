from pydantic import BaseModel, ConfigDict

class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    login: str
    first_name: str
    last_name: str