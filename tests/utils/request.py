from enum import Enum
from typing import Optional

from httpx import AsyncClient

from main import app


class RequestType(Enum):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"


async def make_request(
    url: str,
    token: Optional[str] = None,
    data: Optional[list | dict] = None,
    req_type: RequestType = RequestType.POST,
):
    client_kw = {}
    if token:
        client_kw["headers"] = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(app=app, base_url="http://test", **client_kw) as ac:
        req = getattr(ac, req_type.value)
        kw = {}
        if req_type in (RequestType.POST, RequestType.PUT):
            kw["json"] = data
        response = await req(url, **kw)
    return response.status_code, response.json()
