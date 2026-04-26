from sqlalchemy import select
from core.models import AuditLog


class AuditStore:
    def __init__(self, db): self.db = db
    async def create(self, tenant_id: str, actor: str, action: str, details: dict):
        obj = AuditLog(tenant_id=tenant_id, actor=actor, action=action, details=details)
        self.db.add(obj); await self.db.commit(); return obj
    async def list(self, tenant_id: str):
        r = await self.db.execute(select(AuditLog).where(AuditLog.tenant_id == tenant_id)); return list(r.scalars().all())
