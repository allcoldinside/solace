import uuid
from sqlalchemy import select
from core.models import Case


class CaseStore:
    def __init__(self, db): self.db = db
    async def create(self, tenant_id: str, title: str, description: str):
        c = Case(case_id=f'CASE-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, title=title, description=description)
        self.db.add(c); await self.db.commit(); await self.db.refresh(c); return c
    async def list(self, tenant_id: str):
        r = await self.db.execute(select(Case).where(Case.tenant_id == tenant_id)); return list(r.scalars().all())
    async def get(self, tenant_id: str, case_id: str):
        r = await self.db.execute(select(Case).where(Case.tenant_id == tenant_id, Case.case_id == case_id)); return r.scalar_one_or_none()
