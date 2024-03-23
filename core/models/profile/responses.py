from typing import Optional

from pydantic import BaseModel, EmailStr, Field, AliasChoices

from .enums import ProfileRole
from .db import ProfileDB


class ProfileResponse(ProfileDB):
    phone_number: str | None = Field(
        alias="phoneNumber",
        validation_alias=AliasChoices("phone_number", "phoneNumber"),
    )
    first_name: str | None = Field(
        alias="firstName", validation_alias=AliasChoices("first_name", "firstName")
    )
    last_name: str | None = Field(
        alias="lastName", validation_alias=AliasChoices("last_name", "lastName")
    )
    photo_url: str | None = Field(
        alias="photoUrl", validation_alias=AliasChoices("photo_url", "photoUrl")
    )
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


class UpdateProfileRequest(BaseModel):
    email: EmailStr
    phone_number: Optional[str] = Field(
        alias="phoneNumber",
        validation_alias=AliasChoices("phone_number", "phoneNumber"),
    )
    first_name: str = Field(
        alias="firstName", validation_alias=AliasChoices("first_name", "firstName")
    )
    last_name: str = Field(
        alias="lastName", validation_alias=AliasChoices("last_name", "lastName")
    )

