from fastapi import Request

from services.jwt_auth import decode_token


def id_from_token(request: Request) -> str:
    token = request.headers.get('authorization').split(' ')[1]
    return decode_token(token).get('sub')
