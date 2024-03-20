from pydantic import BaseModel, EmailStr, Field, AliasChoices

from .enums import ProfileRole
from .db import ProfileDB


class ProfileResponse(ProfileDB):
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    photo_url: str | None
    role: str | None


class CreateProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    photo_url: str | None
    role: ProfileRole


class ProfileDetailResponse(BaseModel):
    profile: ProfileResponse
