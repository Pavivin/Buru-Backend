from typing import Mapping
from uuid import UUID

from aiologger import Logger

import container
from apps.api.main_app.v1.services.promo.delete_promo import DeletePromoService


@container.register
class DeletePromoCase:
    def __init__(
        self,
        logger: Logger,
        service: DeletePromoService,
    ):
        self._logger = logger
        self._service = service

    async def __call__(self, promo_id: UUID) -> Mapping:
        await self._service.update_promo(promo_id)
        return {"message": "Промокод удалён успешно"}
