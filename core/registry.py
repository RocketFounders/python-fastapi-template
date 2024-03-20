import datetime
import os
import threading

from core.storage.db import postgres
from core.storage.ping_storage import PingStorage
from core.storage.profile_storage import ProfileStorage

from celery import Celery

server_started = datetime.datetime.now()
VERSION = os.getenv("VERSION", "0")
ENV = os.environ.get("ENV", "LOCAL")

db: postgres.DB = postgres.get_database()
ping_storage = PingStorage(db)
profile_storage = ProfileStorage(db)

CELERY_BROCKER_DSN = os.environ.get("CELERY_BROCKER_DSN", "")
CELERY = Celery(__name__, broker=CELERY_BROCKER_DSN)

CELERY_IS_ACTIVE = os.environ.get("CELERY_IS_ACTIVE", "False").lower().strip() == "true"


async def activate_celery():
    if not CELERY_IS_ACTIVE:
        return
    worker = CELERY.Worker(include=["core.tasks.task_list"])
    thread = threading.Thread(target=worker.start, daemon=True)
    thread.start()
