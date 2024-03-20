import logging

from fastapi import APIRouter, Depends

from core.models.profile.requests import CreateProfileRequest
from core.models.profile.responses import (
    ProfileResponse,
    CreateProfileResponse,
)
from core.services.profile.services import (
    get_current_profile as get_current_profile_service,
    create_profile as create_profile_service,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/current", response_model=ProfileResponse)
async def get_current_profile(
    profile: ProfileResponse = Depends(get_current_profile_service),
):
    return profile


@router.post("/logout")
async def logout(profile: ProfileResponse = Depends(get_current_profile)):
    logger.info(f"User {profile.id} has logged out")
    return {"status": "logged out"}


@router.post("/create", response_model=CreateProfileResponse)
async def create_profile(data: CreateProfileRequest) -> CreateProfileResponse:
    return await create_profile_service(data)
