from typing import Mapping, Optional
from uuid import UUID

import container
from apps.api.main_app import exceptions
from apps.api.main_app.v1.services.sessions import SessionDto
from apps.api.main_app.v1.services.users import UserDto

from . import AbcTokenCase


@container.register
class RefreshTokenCase(AbcTokenCase):
    async def __call__(self, session_id: UUID, user_id: UUID) -> Mapping:
        session: Optional[SessionDto] = await self._sessions.find_session(session_id, user_id)
        if not session:
            raise exceptions.SessionNotFound

        user: UserDto = await self._service.find_by_id(session.user_id)

        access_token, refresh_token = await self._sessions.update_session(session_id=session.id, user_id=user.id)
        await self._log_user(
            info=self._user_logged.TOKEN_REFRESHED, access_token=access_token, refresh_token=refresh_token
        )
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
        }
