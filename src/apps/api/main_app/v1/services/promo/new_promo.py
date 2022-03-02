from uuid import UUID

import asyncpg
from aiologger import Logger
from pydantic import BaseModel

import container
from apps.api.main_app import exceptions
from config import config
from db import PG


class NewPromoDto(BaseModel):
    promo_id: UUID
    promo_code: str


@container.register
class GetPromoService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    @staticmethod
    async def __select_promo(tr: asyncpg.Connection):
        stmt = """
                SELECT promo_id, promo_code
                FROM promocode
                WHERE user_id is null
                AND cur_count > 0
                AND deleted_at is null
                ORDER BY random()
                LIMIT 1
            """
        db_promo = await tr.fetchrow(stmt)
        return db_promo

    @staticmethod
    async def __select_user_promo_count(tr: asyncpg.Connection, user_id: UUID):
        stmt = """
            select count(user_id)
            from promocode
            where user_id = $1
        """
        user_count = await tr.fetchval(stmt, user_id)
        return user_count

    @staticmethod
    async def __update_promo(tr: asyncpg.Connection, user_id: UUID, promo_id: UUID):
        stmt = """
                UPDATE promocode
                SET user_id = $1,
                    updated_at = now(),
                    cur_count = cur_count - 1
                WHERE promo_id = $2
                AND user_id IS NULL
                AND cur_count > 0
                RETURNING *
            """
        status = await tr.fetchval(stmt, user_id, promo_id)
        return status

    async def new_promo(self, user_id: UUID):
        await self._db.start_transaction()
        db_promo = await self.__select_promo(self._db.tx_conn)
        promo = NewPromoDto(**db_promo)
        user_promo_count = await self.__select_user_promo_count(self._db.tx_conn, user_id)

        if user_promo_count > config.max_promo_number_per_user:
            return "Достигнуто максимальное количество промокодов"

        try:
            status = await self.__update_promo(self._db.tx_conn, user_id, promo.promo_id)
            if status == "UPDATE 0":
                raise exceptions.InvalidAnswer("Данные не обновлены, повторите попытку")
            await self._db.tx_ctx.commit()
        except asyncpg.PostgresError as e:
            await self._db.tx_ctx.rollback()
            raise exceptions.InvalidAnswer(e)
        finally:
            self._db.close_transaction()
        return promo.promo_code
