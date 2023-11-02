from fastapi import APIRouter, Depends
from core.models.auth.responses import TokenResponse
from core.services.auth.services import get_access_token


router = APIRouter(tags=['Sign in and Sign up'])


@router.post("/token", response_model=TokenResponse)
async def login(token: TokenResponse = Depends(get_access_token)):
    return token

