from fastapi import APIRouter, Depends

from core.models.profile.responses import ProfileResponse, ProfileDetailResponse, CreateProfileResponse

from core.services.profile.services import \
    get_current_profile as get_current_profile_service, \
    get_profile_detail as get_profile_detail_service, \
    create_profile as create_profile_service

from loguru import logger

router = APIRouter(prefix="/profile", tags=['Profile'])


@router.get("/current", response_model=ProfileResponse)
async def get_current_profile(profile: ProfileResponse = Depends(get_current_profile_service)):
    return profile


@router.post('/logout')
async def logout(current_profile: ProfileResponse = Depends(get_current_profile)):
    logger.info(f'User {current_profile.id} has logged out')
    return {"status": "logged out"}


@router.get("/detail", response_model=ProfileDetailResponse)
async def get_profile_detail(
        detail: ProfileDetailResponse = Depends(get_profile_detail_service)) -> ProfileDetailResponse:
    return detail


@router.post('/create', response_model=CreateProfileResponse)
async def create_profile(profile: CreateProfileResponse = Depends(create_profile_service)) -> CreateProfileResponse:
    return profile
