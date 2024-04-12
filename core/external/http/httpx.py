import urllib.parse

from httpx import AsyncClient

from core.external.http.base import BaseHttpClient, RequestType


class HttpxAsyncClient(BaseHttpClient):
    async_client = None

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def make_request(
        self,
        path: str,
        token: str | None = None,
        data: list | dict | None = None,
        req_type: RequestType = RequestType.POST,
    ):
        client_kw = {}
        if token:
            client_kw["headers"] = {"Authorization": f"Bearer {token}"}
        async with AsyncClient(base_url=self.base_url, **client_kw) as ac:
            req = getattr(ac, req_type.value)
            kw = {}
            if req_type in (RequestType.POST, RequestType.PUT):
                kw["json"] = data
            response = await req(urllib.parse.urljoin(self.base_url, path), **kw)
        return response.status_code, response.json()
