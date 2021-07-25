from fastapi import APIRouter, Request
from fastapi.params import Depends
from queries.profile import select_user, update_user_info
from routes.schema.profile import ProfileSchema
from utils.auth_bearer import JWTBearer
from utils.user_id import id_from_token

profile_router = APIRouter()


@profile_router.get('/profile', response_model=ProfileSchema, dependencies=[Depends(JWTBearer())])
async def get_profile(request: Request) -> str:
    user_id = id_from_token(request)
    return await select_user(user_id)


@profile_router.put('/profile', dependencies=[Depends(JWTBearer())])
async def put_profile(request: Request, schema: ProfileSchema) -> str:
    user_id = id_from_token(request)
    resp = await request.json()
    username = resp.get('username')
    phone = resp.get('phone')
    city = resp.get('city')
    first_name = resp.get('first_name')
    await update_user_info(user_id, username, phone, first_name, city)
    return "The profile was successfully added"
