from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from security.deps import current_user
from storage.entity_store import EntityStore
router = APIRouter(prefix='/entities', tags=['entities'])
@router.get('')
async def list_entities(db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await EntityStore(db).list(user.tenant_id)
