from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    email: str
    password: str

class RegisterUserRequest(BaseModel):
    email: str
    login: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str