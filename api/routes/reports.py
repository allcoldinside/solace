"""Report routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.deps import current_user
from storage.postgres_store import PostgresStore

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("")
async def list_reports(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list[dict]:
    rows = await PostgresStore(db).list_reports(user.tenant_id)
    return [{"report_id": r.report_id, "subject": r.subject, "classification": r.classification, "confidence": r.confidence, "created_at": r.created_at} for r in rows]

@router.get("/{report_id}")
async def get_report(report_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await PostgresStore(db).get_report(user.tenant_id, report_id)
    if row is None:
        raise HTTPException(status_code=404, detail="report not found")
    return {"report_id": row.report_id, "subject": row.subject, "full_markdown": row.full_markdown, "entity_map": row.entity_map, "source_log": row.source_log}
