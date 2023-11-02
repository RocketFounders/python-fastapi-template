from pydantic import Field

from ..profile.db import ProfileDB


class SingUpRequest(ProfileDB):
    id: str | None = Field(default=None, exclude=True)
