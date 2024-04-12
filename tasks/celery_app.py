from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )

    celery_broker_dsn: str | None
    celery_backend_dsn: str | None


celery_config = Settings()

CELERY = Celery(
    __name__,
    broker=celery_config.celery_broker_dsn,
    backend=celery_config.celery_backend_dsn,
    broker_connection_retry_on_startup=True,
)
