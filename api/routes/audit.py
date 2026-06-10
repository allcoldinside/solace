from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from security.deps import require_role
from storage.audit_store import AuditStore
router = APIRouter(prefix='/audit', tags=['audit'])
@router.get('')
async def list_audit(action: str | None = Query(default=None), resource_type: str | None = Query(default=None), db: AsyncSession = Depends(get_db), user=Depends(require_role('admin'))):
    return await AuditStore(db).list(user.tenant_id, action=action, resource_type=resource_type)
