"""Panel routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.deps import current_user
from storage.panel_store import PanelStore

router = APIRouter(prefix="/panel", tags=["panel"])

@router.get("")
async def list_panel(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list[dict]:
    rows = await PanelStore(db).list(user.tenant_id)
    return [{"session_id": r.session_id, "report_id": r.report_id, "status": r.status, "created_at": r.created_at} for r in rows]

@router.get("/{session_id}")
async def get_panel(session_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await PanelStore(db).get(user.tenant_id, session_id)
    if row is None:
        raise HTTPException(status_code=404, detail="panel session not found")
    return {"session_id": row.session_id, "report_id": row.report_id, "transcript": row.transcript, "synthesis": row.synthesis}
