from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, validator


class NewsResponseItem(BaseModel):
    id: Union[str, UUID]
    main_text: str
    user_id: Union[str, UUID]
    topic: Optional[str] = None
    img_link: Optional[str] = None

    @classmethod
    @validator('id', 'user_id', pre=True)
    def uuid_to_str(cls, uuid_id):
        return uuid_id.hex


class NewsResponseSchema(BaseModel):
    news: List[NewsResponseItem]


class NewsRequestSchema(BaseModel):
    main_text: str
    topic: Optional[str] = None
    img_link: Optional[str] = None
