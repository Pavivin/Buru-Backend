from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from apps.api.main_app import exceptions
from config import config

from ..services import auth

security_resolver = HTTPBearer(scheme_name="JWTHeader", auto_error=False)


async def check_token(
    authorization: HTTPAuthorizationCredentials = Security(security_resolver),
) -> bool:
    if not authorization or authorization.credentials != config.secret_token:
        raise exceptions.Unauthorized()
    return True


async def refresh_token_payload(
    authorization: HTTPAuthorizationCredentials = Security(security_resolver),
) -> auth.RefreshTokenPayload:
    if not authorization:
        raise exceptions.Unauthorized()

    rsa_key = config.rsa_public_key
    payload = auth.deserialize_token(authorization.credentials, rsa_key, auth.RefreshTokenPayload)

    assert isinstance(payload, auth.RefreshTokenPayload)

    if payload.type != auth.TokenType.REFRESH:
        raise exceptions.Forbidden()

    return payload


async def access_token_payload(
    authorization: HTTPAuthorizationCredentials = Security(security_resolver),
) -> auth.AccessTokenPayload:
    if not authorization:
        raise exceptions.Unauthorized()

    rsa_key = config.rsa_public_key
    payload = auth.deserialize_token(authorization.credentials, rsa_key, auth.AccessTokenPayload)

    assert isinstance(payload, auth.AccessTokenPayload)

    if payload.type != auth.TokenType.ACCESS:
        raise exceptions.Forbidden()

    return payload
