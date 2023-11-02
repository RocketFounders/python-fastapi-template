from core.utils import throw_server_error
from core.storage.db.postgres import DB


class PingStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def ping(self):
        cursor = await self.db.fetch("SELECT 'pong' AS pong")
        for row in cursor:
            return row["pong"]
        throw_server_error("Unable to ping db")
