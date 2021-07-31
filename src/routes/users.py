from fastapi import APIRouter
from queries.users import all_users
from .schema.users import UsersSchema

users_router = APIRouter()


@users_router.get('/users', response_model=UsersSchema, description='UsersSchema')
async def get_users() -> str:
    users = await all_users()
    return {'users': users}
