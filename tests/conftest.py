import asyncio
import pytest

from core.registry import db
from core.storage.db.postgres import prepare_database


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def async_gen_fixture():
    await db.connect()
    yield
    await db.close()


@pytest.fixture(autouse=True, scope="function")
async def clean():
    await prepare_database(db)
