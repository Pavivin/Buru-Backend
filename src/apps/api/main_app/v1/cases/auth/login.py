from typing import Mapping

import container
from apps.api.main_app import exceptions
from apps.api.main_app.v1.services.users import UserDto

from . import AbcTokenCase


@container.register
class LoginCase(AbcTokenCase):
    async def __call__(self, email: str, password: str) -> Mapping:
        user: UserDto = await self._service.find_by_email(email)
        if not self._service.password_verify(hashed=user.password, plain=password):
            raise exceptions.WrongAuthCredentials

        access_token, refresh_token = await self._sessions.create_session(user_id=user.id)

        await self._log_user(
            info=self._user_logged.LOGIN, access_token=access_token, refresh_token=refresh_token
        )

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
        }
