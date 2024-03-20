import pytest

from core.registry import db
from typing import AsyncGenerator


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True, scope="session")
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
async def async_gen_fixture(anyio_backend: str) -> AsyncGenerator:
    await db.connect()
    yield
    await db.close()


@pytest.fixture(autouse=True, scope="function")
async def clean() -> None:
    assert "localhost" in db.dsn, "Don't even try to do this again!!!"
    with open("../core/storage/db/schema.sql", "r") as f:
        await db.execute(f.read())
        await db.reload_cache()
