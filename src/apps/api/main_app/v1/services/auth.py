from datetime import datetime
from enum import Enum
from json.encoder import JSONEncoder
from typing import Any, Mapping, Tuple, Type, Union
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError, PyJWTError
from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from apps.api.main_app import exceptions
from config import config


class TokenEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        return pydantic_encoder(obj)


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AccessTokenPayload(BaseModel):
    iss: str
    exp: int
    sub: UUID
    sid: UUID
    aud: str
    type: TokenType

    @classmethod
    def create(cls, user_id: UUID, session_id: UUID):
        return cls(
            iss="api",
            exp=int((datetime.utcnow() + config.auth_token_access_ttl).timestamp()),
            sub=user_id,
            sid=session_id,
            aud="user",
            type=TokenType.ACCESS,
        )


class RefreshTokenPayload(BaseModel):
    iss: str
    exp: int
    sub: UUID
    sid: UUID
    aud: str
    type: TokenType

    @classmethod
    def create(cls, user_id: UUID, session_id: UUID):
        return cls(
            iss="api",
            exp=int((datetime.utcnow() + config.auth_token_refresh_ttl).timestamp()),
            sub=user_id,
            sid=session_id,
            aud="user",
            type=TokenType.REFRESH,
        )


def _create_token(
    private_key: str,
    payload: Union[AccessTokenPayload, RefreshTokenPayload],
    algorithm: str = "RS256",
) -> str:
    return jwt.encode(payload.dict(), private_key, algorithm=algorithm, json_encoder=TokenEncoder)


def generate_pair(
    rsa_private_key: str,
    session_id: UUID,
    user_id: UUID,
) -> Tuple[str, str, AccessTokenPayload, RefreshTokenPayload]:
    access_token_payload: AccessTokenPayload = AccessTokenPayload.create(user_id, session_id)
    refresh_token_payload: RefreshTokenPayload = RefreshTokenPayload.create(user_id, session_id)

    return (
        _create_token(rsa_private_key, access_token_payload),
        _create_token(rsa_private_key, refresh_token_payload),
        access_token_payload,
        refresh_token_payload,
    )


def deserialize_token(
    jwt_token: str,
    rsa_public_key: str,
    token_type: Union[Type[AccessTokenPayload], Type[RefreshTokenPayload]],
) -> Union[AccessTokenPayload, RefreshTokenPayload]:
    try:
        decode_jwt: Mapping = jwt.decode(
            jwt_token,
            rsa_public_key,
            algorithms=["RS256"],
            issuer="api",
            audience="user",
        )
    except ExpiredSignatureError as ex:
        if token_type is RefreshTokenPayload:
            raise exceptions.RefreshTokenExpired(debug=str(ex))
        raise exceptions.AccessTokenExpired(debug=str(ex))
    except PyJWTError as ex:
        raise exceptions.Forbidden(debug=str(ex))

    return token_type(**decode_jwt)
