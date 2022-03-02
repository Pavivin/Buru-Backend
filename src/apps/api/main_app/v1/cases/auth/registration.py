from typing import Mapping

import container

from . import AbcTokenCase


@container.register
class RegisterCase(AbcTokenCase):
    async def __call__(self, email: str, password: str) -> Mapping:
        user_id = await self._service.create_user(email, password)
        access_token, refresh_token = await self._sessions.create_session(user_id=user_id)
        await self._log_user(
            info=self._user_logged.REGISTER, access_token=access_token, refresh_token=refresh_token
        )

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
        }
