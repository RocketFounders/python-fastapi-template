from pydantic import computed_field

from core.common import BaseSchema


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str

    @computed_field(alias="access_token", return_type=str)
    def access_token_swagger(self):
        return self.access_token

    @computed_field(alias="token_type", return_type=str)
    def token_type_swagger(self):
        return self.token_type
