from sqlalchemy.ext.asyncio import AsyncSession
from storage.audit_store import AuditStore


async def write_audit(db: AsyncSession, tenant_id: str, actor: str, action: str, details: dict | None = None):
    await AuditStore(db).create(tenant_id=tenant_id, actor=actor, action=action, details=details or {})
