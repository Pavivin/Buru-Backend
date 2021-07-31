from typing import List
from pydantic import BaseModel

from routes.schema.profile import ProfileSchema


class UsersSchema(BaseModel):
    users: List[ProfileSchema]
