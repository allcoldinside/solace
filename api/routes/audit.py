"""Audit routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.deps import require_role
from storage.audit_store import AuditStore

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("")
async def list_audit(db: AsyncSession = Depends(get_db), user=Depends(require_role("admin"))) -> list[dict]:
    rows = await AuditStore(db).list(user.tenant_id)
    return [{"audit_id": r.audit_id, "action": r.action, "resource_type": r.resource_type, "resource_id": r.resource_id, "created_at": r.created_at} for r in rows]
