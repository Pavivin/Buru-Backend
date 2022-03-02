from fastapi import APIRouter, Body, Depends

from apps.api.main_app import exceptions

from ..cases.auth import login, refresh, registration
from ..depends import auth as depends
from ..depends.container import container_resolve
from ..models import auth as model
from ..services import auth

router = APIRouter()
refresh_token_dependency = Depends(depends.refresh_token_payload)


@router.post(
    "/login",
    summary="Аутентификация по email и паролю",
    response_model=model.LoginResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.WrongAuthCredentials,
        ]
    ),
)
async def auth_login(
    data: model.LoginRequest = Body(...), case: login.LoginCase = Depends(container_resolve(login.LoginCase))
):
    return await case(email=data.email, password=data.password)


@router.post(
    "/register",
    summary="Регистрация по email и паролю",
    response_model=model.LoginResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.WrongAuthCredentials,
        ]
    ),
)
async def auth_registration(
    data: model.LoginRequest = Body(...),
    case: registration.RegisterCase = Depends(container_resolve(registration.RegisterCase)),
):
    return await case(email=data.email, password=data.password)


@router.post(
    "/refresh",
    summary="Обновление токена",
    response_model=model.RefreshResponse,
    responses=exceptions.exception_schema(
        [
            exceptions.Unauthorized,
            exceptions.Forbidden,
            exceptions.RefreshTokenExpired,
            exceptions.SessionNotFound,
        ]
    ),
)
async def auth_refresh(
    token: auth.RefreshTokenPayload = refresh_token_dependency,
    case: refresh.RefreshTokenCase = Depends(container_resolve(refresh.RefreshTokenCase)),
):
    return await case(session_id=token.sid, user_id=token.sub)
