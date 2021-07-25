from typing import Optional

from pydantic import BaseModel


class ProfileSchema(BaseModel):
    username: str
    first_name: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
