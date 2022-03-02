from fastapi import APIRouter

from . import endpoints

router = APIRouter()
router.include_router(endpoints.auth.router, prefix="/auth")
router.include_router(endpoints.promo.router, prefix="")
router.include_router(endpoints.notifications.router, prefix="")
