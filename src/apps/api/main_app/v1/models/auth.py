from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic.dataclasses import dataclass

from config import config


class LoginRequest(BaseModel):
    email: EmailStr = Field(config.default_email)
    password: str = Field(config.default_password)


@dataclass(frozen=True)
class ProfileModel:
    id: UUID
    email: EmailStr = Field(config.default_email)


@dataclass(frozen=True)
class LoginResponse:
    accessToken: str
    refreshToken: str


@dataclass(frozen=True)
class RefreshResponse:
    accessToken: str
    refreshToken: str
