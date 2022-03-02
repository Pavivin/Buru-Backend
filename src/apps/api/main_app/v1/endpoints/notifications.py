from typing import List, Mapping

from fastapi import APIRouter, Depends

from apps.api.main_app import exceptions

from ..cases import notifications
from ..depends import auth as depends
from ..depends.container import container_resolve
from ..services import auth

router = APIRouter()
access_token_dependency = Depends(depends.access_token_payload)


@router.get(
    "/notifications",
    summary="Получение уведомлений",
    responses=exceptions.exception_schema(
        [
            exceptions.AuthorizationError,
            exceptions.DatabaseRequestError,
        ]
    ),
)
async def download(
    token: auth.AccessTokenPayload = access_token_dependency,
    case: notifications.GetNotificationsCase = Depends(container_resolve(notifications.GetNotificationsCase)),
) -> List[Mapping]:
    return await case(user_id=token.sub.hex)
