from uuid import UUID

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class UpdatePromoRequest(BaseModel):
    promo_id: UUID
    promo: str


class DeletePromoRequest(BaseModel):
    promo_id: UUID


@dataclass(frozen=True)
class UpdatePromoResponse:
    message: str


@dataclass(frozen=True)
class GetPromoResponse:
    promocode: str
