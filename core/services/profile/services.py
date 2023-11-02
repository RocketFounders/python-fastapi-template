import typing

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from config import CONFIG
from core.models.profile.responses import ProfileResponse, ProfileDetailResponse
from core.registry import profile_storage
from .helpers import oauth2_scheme
from ...models.profile.enums import ProfileRole
from ...models.profile.requests import CreateProfileRequest
from ...models.profile.responses import CreateProfileResponse


async def get_current_profile(token: str = Depends(oauth2_scheme)) -> ProfileResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CONFIG.secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"email": email}
    except JWTError:
        raise credentials_exception
    profile = await profile_storage.get_by_email(email=token_data['email'])
    if profile is None:
        raise credentials_exception
    return profile


async def get_profile_detail(username: str):
    profile = await profile_storage.get_by_username(username=username)
    return ProfileDetailResponse(profile=profile.model_dump())


async def create_profile(data: CreateProfileRequest):
    profile = await profile_storage.create(username=data.username,
                                           password=data.password,
                                           email=data.email,
                                           phone_number=data.phone_number,
                                           first_name=data.first_name,
                                           last_name=data.last_name,
                                           photo_url=data.photo_url,
                                           role=ProfileRole.guest)
    return CreateProfileResponse(id=profile.id,
                                 username=profile.username,
                                 email=profile.email,
                                 phoneNumber=profile.phone_number,
                                 firstName=profile.first_name,
                                 lastName=profile.last_name,
                                 photoUrl=profile.photo_url,
                                 role=profile.role)
