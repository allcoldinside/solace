from sqlalchemy import select
from core.models import Tenant


class TenantStore:
    def __init__(self, db): self.db = db

    async def ensure_default(self, tenant_id: str = 'default'):
        res = await self.db.execute(select(Tenant).where(Tenant.tenant_id == tenant_id))
        t = res.scalar_one_or_none()
        if t:
            return t
        t = Tenant(tenant_id=tenant_id, name=tenant_id)
        self.db.add(t)
        await self.db.commit(); await self.db.refresh(t)
        return t
