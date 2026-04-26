"""Watch routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import WatchCreateRequest
from security.deps import current_user
from storage.watch_store import WatchStore

router = APIRouter(prefix="/watches", tags=["watches"])

@router.get("")
async def list_watches(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list[dict]:
    rows = await WatchStore(db).list(user.tenant_id)
    return [{"watch_id": r.watch_id, "target": r.target, "target_type": r.target_type, "cadence": r.cadence, "is_active": r.is_active} for r in rows]

@router.post("")
async def create_watch(payload: WatchCreateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await WatchStore(db).create(user.tenant_id, payload.target, payload.target_type.value, payload.cadence)
    return {"watch_id": row.watch_id, "target": row.target, "target_type": row.target_type, "cadence": row.cadence}

@router.get("/{watch_id}")
async def get_watch(watch_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await WatchStore(db).get(user.tenant_id, watch_id)
    if row is None:
        raise HTTPException(status_code=404, detail="watch not found")
    return {"watch_id": row.watch_id, "target": row.target, "target_type": row.target_type, "cadence": row.cadence, "is_active": row.is_active}
