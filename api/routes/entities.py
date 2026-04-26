"""Entity routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import EntitySchema
from security.deps import current_user
from storage.entity_store import EntityStore

router = APIRouter(prefix="/entities", tags=["entities"])

@router.get("", response_model=list[EntitySchema])
async def list_entities(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list:
    return await EntityStore(db).list(user.tenant_id)
