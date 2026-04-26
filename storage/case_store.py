"""Case persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Case


class CaseStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tenant_id: str, title: str, description: str = "") -> Case:
        row = Case(tenant_id=tenant_id, title=title, description=description)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def list(self, tenant_id: str) -> list[Case]:
        result = await self.db.execute(select(Case).where(Case.tenant_id == tenant_id).order_by(Case.created_at.desc()))
        return list(result.scalars().all())

    async def get(self, tenant_id: str, case_id: str) -> Case | None:
        result = await self.db.execute(select(Case).where(Case.tenant_id == tenant_id, Case.case_id == case_id))
        return result.scalar_one_or_none()
