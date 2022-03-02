from starlette import status

from apps.api import exceptions

exception_schema = exceptions.exception_schema


class Unauthorized(exceptions.Unauthorized):
    pass


class WrongAuthCredentials(exceptions.ApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Неверный пароль или логин"


class EventNotFound(exceptions.ApiException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Событие не найдено"


class UserNotFound(exceptions.ApiException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Пользователь не найден"


class AccessTokenExpired(exceptions.ApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Access token истёк"


class RefreshTokenExpired(exceptions.ApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Refresh token истёк"


class SessionNotFound(exceptions.ApiException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Сессия не найдена"


class AnswerNotFound(exceptions.ApiException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Ответ не найден"


class InvalidAnswer(exceptions.ApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Невалидный ответ"


class AuthorizationError(exceptions.BusinessException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Неверный токен API."


class Forbidden(exceptions.ApiException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Не хватает прав для выполнения действия"


class DatabaseRequestError(exceptions.ServerException):
    message = "Произошла ошибка при выполнении запроса"
