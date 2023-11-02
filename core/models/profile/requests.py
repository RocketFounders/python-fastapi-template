from pydantic import BaseModel, EmailStr, Field, AliasChoices


class CreateProfileRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str = Field(alias='phoneNumber', validation_alias=AliasChoices('phone_number', 'phoneNumber'))
    first_name: str = Field(alias='firstName', validation_alias=AliasChoices('first_name', 'firstName'))
    last_name: str = Field(alias='lastName', validation_alias=AliasChoices('last_name', 'lastName'))
    photo_url: str | None = Field(alias='photoUrl', validation_alias=AliasChoices('photo_url', 'photoUrl'))
