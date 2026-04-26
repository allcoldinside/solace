from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from security.deps import current_user
from search.engine import search
router = APIRouter(prefix='/search', tags=['search'])
@router.get('')
async def search_route(q: str = Query(''), db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await search(db, user.tenant_id, q)
