from typing import Optional

from pydantic import EmailStr

from .db import ProfileDB
from .enums import ProfileRole
from ...common import BaseSchema


class ProfileResponse(ProfileDB):
    phone_number: str | None
    last_name: str | None
    photo_url: str | None
    role: str | None


class CreateProfileResponse(BaseSchema):
    id: str
    username: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    photo_url: str | None
    role: ProfileRole


class ProfileDetailResponse(BaseSchema):
    profile: ProfileResponse


class UpdateProfileRequest(BaseSchema):
    email: EmailStr
    phone_number: Optional[str]
    first_name: str
    last_name: str
