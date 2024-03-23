from pydantic import BaseModel, EmailStr


class UpdateProfile(BaseModel):
    email: EmailStr
    phone_number: str | None
    first_name: str | None
    last_name: str | None
