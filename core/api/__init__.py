from fastapi import APIRouter
from .profile import profile_router
from .auth import auth_router
from .ping import ping_router


router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(ping_router)

