import uuid

from fastapi import APIRouter, Request
from queries.login import get_password, register_user, user_exist, user_from_login
from routes.schema.login import LoginSchema
from services.jwt_auth import AccessTokenPayload, create_token
from utils.password import check_password_hash, create_password_hash

login_router = APIRouter()


@login_router.post('/login')
async def login(request: Request, body: LoginSchema) -> str:
    record = await request.json()
    username = record.get('username')
    user_password = record.get('user_password')

    password_hash = await get_password(username)

    if not password_hash:
        return f"User with username {username} doesn't exist"

    if check_password_hash(user_password, password_hash):
        user_id = await user_from_login(username)
        access_payload = AccessTokenPayload(sub=user_id)
        token = create_token(access_payload)
        return token
    return "The user_password or username does not match"


@login_router.post('/registration')
async def registration(request: Request, body: LoginSchema) -> str:
    record = await request.json()
    username = record.get('username')
    user_password = record.get('user_password')

    password_hash = create_password_hash(user_password)

    is_user_exist = await user_exist(username)

    if is_user_exist:
        return f"User with name {username} already exist"

    try:
        user_id = uuid.uuid4().hex
        access_payload = AccessTokenPayload(sub=user_id)
        token = create_token(access_payload)
    except ValueError:
        return 'Token Error'

    await register_user(user_id, username, password_hash)
    return token
