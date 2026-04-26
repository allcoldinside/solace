"""System info routes."""

from fastapi import APIRouter, Depends

from config.settings import get_settings
from security.deps import current_user

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/info")
async def info(user=Depends(current_user)) -> dict:
    settings = get_settings()
    return {"service": settings.app_name, "version": settings.version, "environment": settings.environment, "tenant_id": user.tenant_id}
