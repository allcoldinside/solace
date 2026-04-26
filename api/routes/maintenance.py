"""Maintenance routes."""

from fastapi import APIRouter, Depends

from security.deps import require_role

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.get("")
async def maintenance(user=Depends(require_role("admin"))) -> dict:
    return {"status": "ready", "tenant_id": user.tenant_id}
