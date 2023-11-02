import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import List

from asyncpg import (
    CheckViolationError,
    ForeignKeyViolationError,
    UniqueViolationError,
    create_pool,
)

from core.utils import throw_bad_request, throw_server_error

LIMIT_RETRIES = 5
logger = logging.getLogger(__name__)


class DB(ABC):
    dsn = ""

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def fetch(self, query: str, *args):
        raise NotImplementedError

    @abstractmethod
    def fetch_row(self, query: str, *args):
        raise NotImplementedError

    @abstractmethod
    def fetch_val(self, query: str, *args):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query: str, *args):
        raise NotImplementedError

    @abstractmethod
    def execute_many(self, query: str, seq: List):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def reload_cache(self):
        raise NotImplementedError


def get_database() -> DB:
    return AsyncDB(os.getenv("DATABASE_URL"))


class AsyncDB(DB):
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._cursor = None

        self._connection_pool = None

    async def connect(self, retry_counter=0) -> None:
        if not self._connection_pool:
            try:
                self._connection_pool = await create_pool(
                    min_size=1, max_size=20, command_timeout=60, dsn=self.dsn
                )
                retry_counter = 0
                logger.info("Database pool connection opened")
            except Exception as error:
                if retry_counter >= LIMIT_RETRIES:
                    raise error
                retry_counter += 1
                logger.exception(
                    f"got error {str(error).strip()}. reconnecting {retry_counter}"
                )
                await asyncio.sleep(5)
                await self.connect()

    async def __check_connection(self):
        if not self._connection_pool:
            await self.connect()
        return await self._connection_pool.acquire()

    async def fetch(self, query: str, *args) -> List:
        con = await self.__check_connection()
        try:
            result = await con.fetch(query, *args)
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def fetch_row(self, query: str, *args):
        con = await self.__check_connection()
        try:
            result = await con.fetchrow(query, *args)
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def fetch_val(self, query: str, *args):
        con = await self.__check_connection()
        try:
            result = await con.fetchval(query, *args)
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def execute(self, query: str, *args):
        con = await self.__check_connection()
        try:
            result = await con.execute(query, *args)
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def execute_many(self, query: str, seq: List):
        con = await self.__check_connection()
        try:
            result = await con.executemany(query, seq)
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def close(self) -> None:
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
                logger.info("Database pool connection closed")
            except Exception as e:
                logger.exception(e)
                throw_server_error(f"Database exception: {e}")

    async def transaction(self):
        con = await self.__check_connection()
        try:
            return con.transaction
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            throw_server_error(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)

    async def reload_cache(self):
        con = await self.__check_connection()
        try:
            result = await con.reload_schema_state()
            return result
        except (
            ForeignKeyViolationError,
            CheckViolationError,
            UniqueViolationError,
        ) as e:
            logger.exception(f"Database exception: {str(e)}")
            throw_bad_request(f"Database exception: {e}")
        except Exception as e:
            logger.exception(e)
            throw_server_error(f"Database exception: {e}")
        finally:
            await self._connection_pool.release(con)


async def prepare_database(db: DB):
    assert "localhost" in db.dsn, "Don't even try to do this again!!!"
    with open("./core/storage/db/schema.sql", "r") as f:
        await db.execute(f.read())
        await db.reload_cache()
