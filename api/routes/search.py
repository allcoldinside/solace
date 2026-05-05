"""Search route."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import SearchResultSchema
from search.engine import SearchEngine
from security.deps import current_user

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[SearchResultSchema])
async def find(
    q: str = Query(default="", description="Search query"),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user=Depends(current_user),
) -> list[SearchResultSchema]:
    return await SearchEngine(db).query(user.tenant_id, q, limit)
