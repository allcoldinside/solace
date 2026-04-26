from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.models import MemoryEntry
from security.deps import current_user
router = APIRouter(prefix='/memory', tags=['memory'])
@router.get('')
async def list_memory(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(MemoryEntry).where(MemoryEntry.tenant_id == user.tenant_id)); return list(r.scalars().all())
