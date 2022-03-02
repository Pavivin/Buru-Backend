from abc import ABC, abstractmethod
from enum import Enum
from typing import Mapping

from aiologger import Logger

from apps.api.main_app.v1.services.sessions import SessionService
from apps.api.main_app.v1.services.users import UserService


class UserLogged(Enum):
    LOGIN = "user_login"
    REGISTER = "user_registered"
    TOKEN_REFRESHED = "user_token_refreshed"


class AbcTokenCase(ABC):
    def __init__(
        self,
        logger: Logger,
        service: UserService,
        sessions: SessionService,
    ):
        self._logger = logger
        self._service = service
        self._sessions = sessions

    @property
    def _user_logged(self):
        return UserLogged

    async def _log_user(self, info: UserLogged, access_token: str, refresh_token: str) -> None:
        await self._logger.info(
            info,
            extra={
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )

    @abstractmethod
    async def __call__(self) -> Mapping:
        ...
