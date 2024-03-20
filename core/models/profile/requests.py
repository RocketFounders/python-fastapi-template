from pydantic import BaseModel, EmailStr, Field, AliasChoices


class CreateProfileRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    photo_url: str | None
