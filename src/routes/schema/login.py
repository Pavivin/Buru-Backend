from pydantic import BaseModel
from pydantic.fields import Field


class LoginSchema(BaseModel):
    username: str = Field()
    user_password: str = Field()
