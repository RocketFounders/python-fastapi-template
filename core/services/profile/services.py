from core.models.profile.domains import UpdateProfile
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from config import CONFIG
from core.models.profile.responses import ProfileResponse, UpdateProfileRequest
from core.registry import profile_storage
from .helpers import oauth2_scheme
from ...models.profile.enums import ProfileRole
from ...models.profile.requests import CreateProfileRequest
from ...models.profile.responses import CreateProfileResponse

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_profile(token: str = Depends(oauth2_scheme)) -> ProfileResponse:
    try:
        payload = jwt.decode(token, CONFIG.secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = {"email": email}
    except JWTError:
        raise credentials_exception
    profile = await profile_storage.get_by_email(email=token_data["email"])
    if not profile:
        raise credentials_exception
    return profile


async def create_profile(data: CreateProfileRequest):
    profile = await profile_storage.create(
        **data.dict(),
        role=ProfileRole.guest,
    )
    return CreateProfileResponse(**profile)


async def get_all_profiles(
    token: str = Depends(oauth2_scheme),
) -> list[ProfileResponse]:
    return await profile_storage.get_all()


async def update_profile_service(
    update_request: UpdateProfileRequest, token: str = Depends(oauth2_scheme)
) -> ProfileResponse:
    try:
        payload = jwt.decode(token, CONFIG.secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    profile_update = UpdateProfile(**update_request.model_dump())
    return await profile_storage.update(profile_update, email)
