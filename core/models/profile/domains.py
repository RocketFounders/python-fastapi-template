from pydantic import EmailStr

from core.common import BaseSchema


class UpdateProfile(BaseSchema):
    email: EmailStr
    phone_number: str | None
    first_name: str | None
    last_name: str | None
