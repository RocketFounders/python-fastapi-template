from abc import ABC
from enum import Enum


class RequestType(Enum):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"


class BaseHttpClient(ABC):
    base_url: str

    def make_request(
        self,
        path: str,
        token: str | None = None,
        data: list | dict | None = None,
        req_type: RequestType = RequestType.POST,
    ):
        raise NotImplementedError
