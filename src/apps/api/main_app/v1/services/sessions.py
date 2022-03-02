from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID, uuid4

from aiologger import Logger
from pydantic import BaseModel

import container
from config import config
from db import PG

from ..services import auth


class SessionDto(BaseModel):
    id: UUID
    user_id: UUID
    expires_at: datetime


@container.register
class SessionService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    async def create_session(self, *, user_id: UUID) -> Tuple[str, str]:
        private_key = config.rsa_private_key
        session_id = uuid4()

        access_token, refresh_token, _, refresh_token_payload = auth.generate_pair(private_key, session_id, user_id)

        stmt = """
            INSERT INTO user_sessions(id, user_id, expires_at)
            VALUES ($1, $2, $3)
        """
        expires_at = datetime.fromtimestamp(refresh_token_payload.exp)
        await self._db.execute(stmt, session_id, user_id, expires_at)

        await self._logger.info(
            "user_session_created",
            extra={
                "session": {
                    "id": session_id.hex,
                    "expires_at": expires_at,
                },
                "user": {
                    "id": user_id.hex,
                },
            },
        )
        return access_token, refresh_token

    async def find_session(self, session_id: UUID, user_id: UUID) -> Optional[SessionDto]:
        stmt = """
            SELECT *
            FROM user_sessions
            WHERE id = $1 AND user_id = $2
        """
        row = await self._db.fetchrow(stmt, session_id, user_id)
        if row:
            return SessionDto(**row)
        return None

    async def update_session(self, session_id: UUID, user_id: UUID) -> Tuple[str, str]:
        private_key = config.rsa_private_key
        access_token, refresh_token, _, refresh_token_payload = auth.generate_pair(private_key, session_id, user_id)
        stmt = """
            UPDATE user_sessions
            SET expires_at = $1
            WHERE id = $2
        """
        expires_at = datetime.fromtimestamp(refresh_token_payload.exp, tz=timezone.utc)
        await self._db.execute(stmt, expires_at, session_id)

        await self._logger.info(
            "user_session_updated",
            extra={
                "session": {
                    "id": session_id.hex,
                    "expires_at": expires_at.isoformat(),
                },
                "user": {
                    "id": user_id.hex,
                },
            },
        )

        return access_token, refresh_token
