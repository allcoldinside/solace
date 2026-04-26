"""Graph route."""

from fastapi import APIRouter, Depends

from security.deps import current_user

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("")
async def get_graph(user=Depends(current_user)) -> dict:
    return {"tenant_id": user.tenant_id, "nodes": [], "edges": [], "message": "graph backend stub ready"}
