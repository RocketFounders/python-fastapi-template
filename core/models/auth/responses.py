from pydantic import BaseModel, Field, AliasChoices, computed_field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    @computed_field(alias="access_token", return_type=str)
    def access_token_swagger(self):
        return self.access_token

    @computed_field(alias="token_type", return_type=str)
    def token_type_swagger(self):
        return self.token_type
