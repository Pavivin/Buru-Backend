from typing import List, Mapping

from aiologger import Logger

import container
from broker.consumer import consume
from db import PG


@container.register
class NotificationService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    @staticmethod
    async def get_notifications(user_id) -> List[Mapping]:
        while True:
            msg = []
            async for item in consume(user_id=user_id):
                msg.append(item)
            return msg
