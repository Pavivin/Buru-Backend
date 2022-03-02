from uuid import UUID

import asyncpg
from aiologger import Logger

import container
from apps.api.main_app import exceptions
from db import PG


@container.register
class DeletePromoService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    @staticmethod
    async def __delete_promo(tr: asyncpg.Connection, promo_id: UUID):
        stmt = """
                UPDATE promocode
                SET deleted_at = now()
                WHERE promo_id = $1
            """
        await tr.execute(stmt, promo_id)

    async def update_promo(self, promo_id: UUID):
        await self._db.start_transaction()

        try:
            await self.__delete_promo(self._db.tx_conn, promo_id)
            await self._db.tx_ctx.commit()
        except asyncpg.PostgresError as e:
            await self._db.tx_ctx.rollback()
            raise exceptions.InvalidAnswer(e)
        finally:
            self._db.close_transaction()
