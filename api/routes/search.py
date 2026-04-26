"""Search route."""

from fastapi import APIRouter, Depends, Query

from core.schemas import SearchResultSchema
from security.deps import current_user

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=list[SearchResultSchema])
async def find(q: str = Query(default=""), user=Depends(current_user)) -> list[SearchResultSchema]:
    if not q:
        return []
    return [SearchResultSchema(id="LOCAL", type="system", title="Search ready", snippet=f"tenant={user.tenant_id}", score=1.0)]
