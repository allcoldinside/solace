from sqlalchemy import select
from core.models import Tenant


class TenantStore:
    def __init__(self, db): self.db = db

    async def ensure_default(self, tenant_id: str = 'default') -> Tenant:
        res = await self.db.execute(select(Tenant).where(Tenant.tenant_id == tenant_id))
        t = res.scalar_one_or_none()
        if t:
            return t
        t = Tenant(tenant_id=tenant_id, name=tenant_id)
        self.db.add(t)
        await self.db.commit(); await self.db.refresh(t)
        return t

    async def get(self, tenant_id: str) -> Tenant | None:
        res = await self.db.execute(select(Tenant).where(Tenant.tenant_id == tenant_id))
        return res.scalar_one_or_none()

    async def list_all(self) -> list:
        res = await self.db.execute(select(Tenant))
        return list(res.scalars().all())
