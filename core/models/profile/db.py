from core.common import BaseSchema


class ProfileDB(BaseSchema):
    id: str | None
    username: str | None
    password: str | None
    email: str | None
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    photo_url: str | None
    role: str | None
    is_internal: bool | None
