"""Memory routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from memory.service import MemoryService
from security.deps import current_user

router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("")
async def list_memory(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list[dict]:
    rows = await MemoryService(db).list(user.tenant_id)
    return [{"memory_id": r.memory_id, "report_id": r.report_id, "entity_id": r.entity_id, "content": r.content, "tags": r.tags, "created_at": r.created_at} for r in rows]
