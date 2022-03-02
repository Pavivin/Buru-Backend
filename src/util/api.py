from typing import Any

import ujson
from aiologger import Logger
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

from container import container


async def request_logger(request: Request):
    logger = container.resolve(Logger)
    headers = {key: request.headers.getlist(key) for key in request.headers.keys()}
    query_params = dict(request.query_params.items())
    path_params = dict(request.path_params.items())

    body = ""
    if "application/json" in request.headers.getlist("Content-Type"):
        body = ujson.dumps(await request.json())

    await logger.info(
        "api_request",
        extra={
            "request": {
                "headers": ujson.dumps(headers),
                "body": body,
                "query_params": ujson.dumps(query_params),
                "path_params": ujson.dumps(path_params),
                "url": request.url.path,
                "method": request.method,
                "base_url": request.base_url.hostname,
            }
        },
    )


def jsonable_encode(obj: Any) -> Any:
    return jsonable_encoder(obj)
