from typing import Any, Dict, List, Mapping, Optional, Type

from starlette import status


def exception_schema(exceptions: List[Type["ApiException"]]):
    responses: Dict[int, Dict] = {}

    schema = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "title": "Код ошибки",
            },
            "message": {
                "type": "string",
                "title": "Описание ошибки",
            },
            "payload": {"type": "object", "title": "Тело ошибки"},
            "debug": {
                "type": "string",
                "title": "Debug информация (traceback или что-то еще)",
            },
        },
    }

    for exc in exceptions:
        code = exc.code()

        if exc.status_code not in responses:
            responses[exc.status_code] = {}

        responses[exc.status_code][code] = {"value": {"code": code, "message": exc.message}}

    return {
        status_code: {"content": {"application/json": {"schema": schema, "examples": examples}}}
        for status_code, examples in responses.items()
    }


class ApiException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Упс! Что-то пошло не так ;("

    def __init__(
        self,
        message: Optional[str] = None,
        payload: Optional[Mapping] = None,
        debug: Any = None,
    ):
        self.message = message or self.message
        self.payload = payload
        self.debug = debug

    @classmethod
    def code(cls):
        return cls.__name__

    def to_json(self) -> Mapping:
        return {
            "code": self.code(),
            "message": self.message,
            "payload": self.payload,
            "debug": self.debug,
        }


class BusinessException(ApiException):
    status_code = 500
    message = "Упс! Что-то пошло не так ;("


class ServerException(ApiException):
    status_code = 500
    message = "Упс! Что-то пошло не так ;("


class Unauthorized(ApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Вы не авторизованы"
