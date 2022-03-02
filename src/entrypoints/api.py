# pylint: disable=unused-argument
import time
from typing import Set

import uvicorn
from aiologger import Logger
from fastapi import FastAPI
from fastapi.responses import Response, UJSONResponse
from starlette.requests import Request

import application
from apps.api import exceptions, main_app
from config import config
from container import container

IGNORED_ENVIRONMENTS: Set[str] = {"local", "pytest"}


app = FastAPI(
    title=config.title,
    version=config.version,
    docs_url=config.docs_url,
    redoc_url=config.redoc_url,
    openapi_url=config.openapi_url,
)

app.include_router(main_app.router, prefix="/api/main")


@app.on_event("startup")
async def on_startup():
    await application.on_startup()


@app.on_event("shutdown")
async def on_shutdown():
    await application.on_shutdown()


@app.middleware("http")
async def request_execution_time(request: Request, call_next):
    start = time.perf_counter()
    logger: Logger = container.resolve(Logger)
    response: Response = await call_next(request)
    await logger.info(
        f"execution_time_ms {round((time.perf_counter() - start) * 1000)}",
    )
    return response


@app.exception_handler(Exception)
async def unicorn_base_exception_handler(request: Request, exc: Exception):
    error = exceptions.ServerException(debug=str(exc))

    return UJSONResponse(
        status_code=error.status_code,
        content=error.to_json(),
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(request: Request, exc: exceptions.ApiException):
    return UJSONResponse(status_code=exc.status_code, content=exc.to_json())


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8001)
