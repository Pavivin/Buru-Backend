from fastapi import FastAPI

from .info import info_router
from .news import news_router
from .profile import profile_router
from .login import login_router
from .chat import chat_router


def setup_routes(app: FastAPI) -> None:
    app.include_router(login_router)
    app.include_router(profile_router)
    app.include_router(news_router)
    app.include_router(info_router)
    app.include_router(chat_router)
