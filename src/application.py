from aiologger import Logger

from config import config
from container import container
from db import PG


async def on_startup():
    pg = PG()
    logger = Logger.with_default_handlers(name="app")
    await pg.init(dsn=config.postgres_dsn)
    container.register(Logger, instance=logger)
    container.register(PG, instance=pg)


async def on_shutdown():
    db: PG = container.resolve(PG)
    await db.close()
