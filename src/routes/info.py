from fastapi import APIRouter
from settings import APP_ID, AUDIENCE, VERSION

info_router = APIRouter()


@info_router.get('/')
async def info() -> str:
    return f"{AUDIENCE} {APP_ID}, version: {VERSION}"
