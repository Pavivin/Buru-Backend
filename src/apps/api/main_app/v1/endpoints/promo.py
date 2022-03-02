# pylint: disable=unused-argument
from fastapi import APIRouter, Body, Depends

from apps.api.main_app import exceptions

from ..cases.promo import delete_promo, get_promo, update_promo
from ..depends import auth as depends
from ..depends.container import container_resolve
from ..models import promo as model
from ..services import auth

router = APIRouter()
access_token_dependency = Depends(depends.access_token_payload)


@router.get(
    "/promo",
    summary="Получение промокода",
    response_model=model.GetPromoResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.WrongAuthCredentials,
        ]
    ),
)
async def get_promo_route(
    token: auth.AccessTokenPayload = access_token_dependency,
    case: get_promo.GetPromoCase = Depends(container_resolve(get_promo.GetPromoCase)),
):
    return await case(token)


@router.put(
    "/promo",
    summary="Обновление промокода",
    response_model=model.UpdatePromoResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.WrongAuthCredentials,
        ]
    ),
)
async def update_promo_route(
    data: model.UpdatePromoRequest = Body(...),
    token: auth.AccessTokenPayload = access_token_dependency,
    case: update_promo.UpdatePromoCase = Depends(container_resolve(update_promo.UpdatePromoCase)),
):
    return await case(promo_id=data.promo_id, code=data.promo)


@router.delete(
    "/promo",
    summary="Удаление промокода",
    response_model=model.UpdatePromoResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.WrongAuthCredentials,
        ]
    ),
)
async def delete_promo_route(
    data: model.DeletePromoRequest = Body(...),
    token: auth.AccessTokenPayload = access_token_dependency,
    case: delete_promo.DeletePromoCase = Depends(container_resolve(delete_promo.DeletePromoCase)),
):
    return await case(promo_id=data.promo_id)
