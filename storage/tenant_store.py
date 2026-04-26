"""Tenant persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tenant


class TenantStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(self, tenant_id: str = "default", name: str | None = None) -> Tenant:
        result = await self.db.execute(select(Tenant).where(Tenant.tenant_id == tenant_id))
        row = result.scalar_one_or_none()
        if row is not None:
            return row
        row = Tenant(tenant_id=tenant_id, name=name or tenant_id)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def create(self, tenant_id: str, name: str) -> Tenant:
        row = Tenant(tenant_id=tenant_id, name=name)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row
