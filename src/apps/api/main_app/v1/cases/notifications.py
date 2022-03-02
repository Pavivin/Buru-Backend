from typing import List, Mapping

from aiologger import Logger

import container
from apps.api.main_app.v1.services.notifications import NotificationService


@container.register
class GetNotificationsCase:
    def __init__(
        self,
        logger: Logger,
        service: NotificationService,
    ):
        self._logger = logger
        self._service = service

    async def __call__(self, user_id: str) -> List[Mapping]:
        return await self._service.get_notifications(user_id)
