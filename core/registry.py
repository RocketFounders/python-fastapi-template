import datetime
import os

from core.storage.db import postgres
from core.storage.ping_storage import PingStorage
from core.storage.profile_storage import ProfileStorage

server_started = datetime.datetime.now()
VERSION = os.getenv("VERSION", "0")
ENV = os.environ.get("ENV", "LOCAL")

db: postgres.DB = postgres.get_database()
ping_storage = PingStorage(db)
profile_storage = ProfileStorage(db)
