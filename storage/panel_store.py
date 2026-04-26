import uuid
from sqlalchemy import select
from core.models import PanelSessionRecord


class PanelStore:
    def __init__(self, db): self.db = db
    async def create(self, tenant_id: str, report_id: str, summary: str, transcript: list):
        s = PanelSessionRecord(session_id=f'SESSION-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, report_id=report_id, summary=summary, transcript=transcript)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s); return s
    async def list(self, tenant_id: str):
        r = await self.db.execute(select(PanelSessionRecord).where(PanelSessionRecord.tenant_id == tenant_id)); return list(r.scalars().all())
    async def get(self, tenant_id: str, session_id: str):
        r = await self.db.execute(select(PanelSessionRecord).where(PanelSessionRecord.tenant_id == tenant_id, PanelSessionRecord.session_id == session_id)); return r.scalar_one_or_none()
