"""Memory service."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MemoryEntry
from reports.schema import ReportData


class MemoryService:
    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    async def remember_report(self, tenant_id: str, report: ReportData) -> MemoryEntry | dict:
        data = {"tenant_id": tenant_id, "report_id": report.report_id, "content": report.executive_summary, "tags": [report.subject_type, report.confidence]}
        if self.db is None:
            return data
        entry = MemoryEntry(**data)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def list(self, tenant_id: str, limit: int = 50) -> list[MemoryEntry]:
        if self.db is None:
            return []
        result = await self.db.execute(select(MemoryEntry).where(MemoryEntry.tenant_id == tenant_id).order_by(MemoryEntry.created_at.desc()).limit(limit))
        return list(result.scalars().all())
