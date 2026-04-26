from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import WatchCreateRequest
from security.deps import current_user
from storage.watch_store import WatchStore
router = APIRouter(prefix='/watches', tags=['watches'])
@router.get('')
async def list_watches(db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await WatchStore(db).list(user.tenant_id)
@router.post('')
async def create_watch(payload: WatchCreateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await WatchStore(db).create(user.tenant_id, payload.target, payload.target_type.value)
@router.get('/{watch_id}')
async def get_watch(watch_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    x = await WatchStore(db).get(user.tenant_id, watch_id)
    if not x: raise HTTPException(status_code=404, detail='not found')
    return x
