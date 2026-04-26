"""Watch persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import WatchRecord


class WatchStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tenant_id: str, target: str, target_type: str = "unknown", cadence: str = "daily") -> WatchRecord:
        row = WatchRecord(tenant_id=tenant_id, target=target, target_type=target_type, cadence=cadence)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def list(self, tenant_id: str) -> list[WatchRecord]:
        result = await self.db.execute(select(WatchRecord).where(WatchRecord.tenant_id == tenant_id).order_by(WatchRecord.created_at.desc()))
        return list(result.scalars().all())

    async def get(self, tenant_id: str, watch_id: str) -> WatchRecord | None:
        result = await self.db.execute(select(WatchRecord).where(WatchRecord.tenant_id == tenant_id, WatchRecord.watch_id == watch_id))
        return result.scalar_one_or_none()
