from datetime import datetime
from uuid import UUID

import asyncpg
from aiologger import Logger
from pydantic import BaseModel

import container
from apps.api.main_app import exceptions
from db import PG


class UpdatePromoDto(BaseModel):
    promo_id: UUID
    promo_code: str
    created_at: datetime


@container.register
class UpdatePromoService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    @staticmethod
    async def __select_promo(tr: asyncpg.Connection, promo_id: UUID):
        stmt = """
                SELECT promo_id, promo_code, created_at
                FROM promocode
                WHERE promo_id = $1
            """
        db_promo = await tr.fetchrow(stmt, promo_id)
        return db_promo

    @staticmethod
    async def __update_promo(tr: asyncpg.Connection, code: str, promo_id: UUID, created_at: datetime):
        stmt = """
                UPDATE promocode
                    SET promo_code = $1,
                    updated_at = now()
                WHERE promo_id = $2
                AND created_at = $3
                RETURNING *
            """
        status = await tr.fetchval(stmt, code, promo_id, created_at)
        return status

    async def update_promo(self, promo_id: UUID, code: str):
        await self._db.start_transaction()
        db_promo = await self.__select_promo(self._db.tx_conn, promo_id)
        promo = UpdatePromoDto(**db_promo)

        try:
            update_status = await self.__update_promo(self._db.tx_conn, code, promo.promo_id, promo.created_at)
            if update_status == "UPDATE 0":
                raise exceptions.InvalidAnswer("Ошибка во время выполнения. Обновите данные")
            await self._db.tx_ctx.commit()
        except asyncpg.PostgresError as e:
            await self._db.tx_ctx.rollback()
            raise exceptions.InvalidAnswer(e)
        finally:
            self._db.close_transaction()
        return promo.promo_code
