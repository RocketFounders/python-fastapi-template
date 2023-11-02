from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from config import CONFIG
from core.models.auth.responses import TokenResponse
from core.models.profile.db import ProfileDB
from core.registry import profile_storage
from core.utils import throw_bad_request

from ..profile.helpers import verify_password, create_access_token


def get_token(profile: ProfileDB) -> str:
    started_at = datetime.utcnow()
    token_expires = started_at + timedelta(days=CONFIG.access_token_expire_days)
    token = create_access_token(
        data={"sub": str(profile.email), "exp": token_expires}
    )
    return token


async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    profile = await profile_storage.get_by_email(form_data.username)
    if not verify_password(form_data.password, profile.password):
        raise throw_bad_request("Invalid username or password")
    token = get_token(profile)
    print('token', token)
    return TokenResponse(access_token=token, token_type="bearer")
