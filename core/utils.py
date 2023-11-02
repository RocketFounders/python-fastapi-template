from fastapi import HTTPException
from starlette import status


def throw_server_error(message: str):
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


def throw_bad_request(message: str):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, message)


def throw_not_found(message: str):
    raise HTTPException(status.HTTP_404_NOT_FOUND, message)


def throw_failed_dependency(message: str):
    raise HTTPException(status.HTTP_424_FAILED_DEPENDENCY, message)


def throw_credential_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
