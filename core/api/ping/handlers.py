from fastapi import APIRouter

from core.registry import ping_storage, server_started, VERSION

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/")
async def ping() -> dict[str, str]:
    return {
        "ping": await ping_storage.ping(),
        "server_started": str(server_started),
        "version": VERSION,
    }
