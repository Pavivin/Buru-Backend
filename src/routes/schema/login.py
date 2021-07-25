from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    user_password: str
