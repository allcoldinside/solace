from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from security.deps import current_user
from core.database import get_db
from storage.panel_store import PanelStore
router = APIRouter(prefix='/panel', tags=['panel'])
@router.get('')
async def list_panel(db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await PanelStore(db).list(user.tenant_id)
@router.get('/{session_id}')
async def get_panel(session_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    x = await PanelStore(db).get(user.tenant_id, session_id)
    if not x: raise HTTPException(status_code=404, detail='not found')
    return x
