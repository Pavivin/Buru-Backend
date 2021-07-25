import time
import uuid
from dataclasses import asdict, dataclass
from typing import Optional

import jwt
import settings


@dataclass
class AccessTokenPayload:
    """
        Access JWT
    """
    sub: str
    sid: str = uuid.uuid4().hex
    phone: Optional[str] = None
    email: Optional[str] = None
    aud: str = settings.AUDIENCE
    iss: str = settings.APP_ID
    exp: int = int(time.time()) + settings.REFRESH_TOKEN_TTL_SECONDS


@dataclass
class RefreshTokenPayload:
    """
        Refresh JWT
    """
    rid: str
    sub: str
    sid: str = uuid.uuid4().hex
    iss: str = settings.APP_ID
    exp: int = int(time.time()) + settings.REFRESH_TOKEN_TTL_SECONDS


def create_token(payload: AccessTokenPayload) -> str:
    return jwt.encode(asdict(payload), settings.SECRET_KEY, algorithm=settings.ALGORITHMS_JWT)


def decode_token(encoded: str) -> dict:
    return jwt.decode(encoded, settings.SECRET_KEY, algorithms=[settings.ALGORITHMS_JWT], audience=settings.AUDIENCE)
