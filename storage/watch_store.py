import uuid
from sqlalchemy import select
from core.models import WatchRecord


class WatchStore:
    def __init__(self, db): self.db = db
    async def create(self, tenant_id: str, target: str, target_type: str):
        w = WatchRecord(watch_id=f'WATCH-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, target=target, target_type=target_type)
        self.db.add(w); await self.db.commit(); await self.db.refresh(w); return w
    async def list(self, tenant_id: str):
        r = await self.db.execute(select(WatchRecord).where(WatchRecord.tenant_id == tenant_id)); return list(r.scalars().all())
    async def get(self, tenant_id: str, watch_id: str):
        r = await self.db.execute(select(WatchRecord).where(WatchRecord.tenant_id == tenant_id, WatchRecord.watch_id == watch_id)); return r.scalar_one_or_none()
