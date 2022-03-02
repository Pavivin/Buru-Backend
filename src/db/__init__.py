import asyncio
from contextvars import ContextVar
from typing import Any, AsyncIterator, List, Optional

import asyncpg
import ujson

_TRANSACTION: ContextVar[Optional[asyncpg.connection.Connection]] = ContextVar("TRANSACTION", default=None)


class TransactionContext:
    __slots__ = ["__pool", "__connection_ctx", "__transaction", "isolation"]

    def __init__(self, pool: asyncpg.pool.Pool, isolation: str):
        self.__pool = pool
        self.__connection_ctx = None
        self.__transaction = None
        self.isolation = isolation

    async def __aenter__(self):
        self.__connection_ctx = self.__pool.acquire()
        connection: asyncpg.connection.Connection = await self.__connection_ctx.__aenter__()
        self.__transaction = connection.transaction(isolation=self.isolation)
        try:
            await self.__transaction.__aenter__()
        except Exception:
            await asyncio.shield(self.__connection_ctx.__aexit__())
            raise

        return connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async def _close():
            try:
                await self.__transaction.__aexit__(exc_type, exc_val, exc_tb)
            finally:
                await self.__connection_ctx.__aexit__(exc_type, exc_val, exc_tb)

        await asyncio.shield(_close())

    async def commit(self):
        await asyncio.shield(self.__transaction.commit())


class PG:
    __slots__ = ("__pool", "tx_ctx", "tx_conn")

    def __init__(self):
        self.__pool = None
        self.tx_ctx = None
        self.tx_conn: asyncpg.Connection | None = None

    @property
    def pool(self) -> asyncpg.pool.Pool:
        assert self.__pool, "Pool is not initialized"
        return self.__pool

    @staticmethod
    def _connection_init():
        async def wrapper(connection: asyncpg.Connection):
            await connection.set_type_codec("json", schema="pg_catalog", encoder=ujson.dumps, decoder=ujson.loads)
            await connection.set_type_codec("jsonb", schema="pg_catalog", encoder=ujson.dumps, decoder=ujson.loads)

        return wrapper

    @staticmethod
    def _connection_setup():
        async def wrapper(connection: asyncpg.pool.PoolConnectionProxy):  # pylint: disable=unused-argument
            pass

        return wrapper

    async def init(self, dsn: str):
        self.__pool = await asyncpg.create_pool(dsn=dsn, init=self._connection_init(), setup=self._connection_setup())

    async def close(self):
        await self.pool.close()
        self.__pool = None

    async def fetch(self, query: str, *args, timeout: Optional[float] = None) -> List[asyncpg.Record]:
        method = getattr(_TRANSACTION.get(), "fetch", self.pool.fetch)
        result: List[asyncpg.Record] = await method(query, *args, timeout=timeout)
        return result

    async def fetchrow(self, query: str, *args, timeout: Optional[float] = None) -> asyncpg.Record:
        method = getattr(_TRANSACTION.get(), "fetchrow", self.pool.fetchrow)
        return await method(query, *args, timeout=timeout)

    async def fetchval(self, query: str, *args, timeout: Optional[float] = None) -> Any:
        method = getattr(_TRANSACTION.get(), "fetchval", self.pool.fetchval)
        return await method(query, *args, timeout=timeout)

    async def execute(self, query: str, *args, timeout: Optional[float] = None):
        method = getattr(_TRANSACTION.get(), "execute", self.pool.execute)
        return await method(query, *args, timeout=timeout)

    async def executemany(self, query: str, *args, timeout: Optional[float] = None):
        method = getattr(_TRANSACTION.get(), "executemany", self.pool.executemany)
        return await method(query, *args, timeout=timeout)

    async def start_transaction(self, isolation="read_committed") -> None:
        assert self.tx_ctx is None, "Transaction already started"

        self.tx_conn = await self.pool.acquire()
        self.tx_ctx = self.tx_conn.transaction(isolation=isolation)
        await self.tx_ctx.start()

    def close_transaction(self) -> None:
        self.tx_ctx = None
        self.tx_conn = None

    async def get_transaction(self) -> asyncpg.Connection:
        async with self.pool.acquire() as conn:
            return conn

    async def cursor(self, query: str) -> AsyncIterator[asyncpg.Record]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                cursor = await connection.cursor(query)
                while row := await cursor.fetchrow():  # noqa: E203, E701, E231
                    yield row
