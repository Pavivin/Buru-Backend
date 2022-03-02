from typing import Mapping
from uuid import UUID

from aiologger import Logger

import container
from apps.api.main_app.v1.services.promo.update_promo import UpdatePromoService


@container.register
class UpdatePromoCase:
    def __init__(
        self,
        logger: Logger,
        service: UpdatePromoService,
    ):
        self._logger = logger
        self._service = service

    async def __call__(self, promo_id: UUID, code: str) -> Mapping:
        await self._service.update_promo(promo_id, code)
        return {"message": "Промокод обновлён успешно"}
