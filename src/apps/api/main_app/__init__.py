from fastapi import APIRouter
from fastapi.responses import UJSONResponse

from . import v1

router = APIRouter()
router.include_router(v1.router, prefix="/v1", default_response_class=UJSONResponse, tags=["app"])
