from pydantic import EmailStr

from core.common import BaseSchema


class CreateProfileRequest(BaseSchema):
    username: str
    password: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    photo_url: str | None
