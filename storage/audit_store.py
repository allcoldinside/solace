from sqlalchemy import select

from core.models import AuditLog


class AuditStore:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        tenant_id: str,
        actor_user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        metadata_json: dict,
        request_id: str,
        ip_address: str,
        user_agent: str,
    ):
        obj = AuditLog(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata_json=metadata_json,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def list(self, tenant_id: str, action: str | None = None, resource_type: str | None = None):
        q = select(AuditLog).where(AuditLog.tenant_id == tenant_id)
        if action:
            q = q.where(AuditLog.action == action)
        if resource_type:
            q = q.where(AuditLog.resource_type == resource_type)
        r = await self.db.execute(q.order_by(AuditLog.created_at.desc()))
        return list(r.scalars().all())
