from typing import Mapping

from aiologger import Logger

import container
from apps.api.main_app.v1.services.auth import AccessTokenPayload
from apps.api.main_app.v1.services.promo.new_promo import GetPromoService


@container.register
class GetPromoCase:
    def __init__(
        self,
        logger: Logger,
        service: GetPromoService,
    ):
        self._logger = logger
        self._service = service

    async def __call__(self, token: AccessTokenPayload) -> Mapping:
        promo = await self._service.new_promo(token.sub)
        return {"promocode": promo}
