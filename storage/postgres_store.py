"""Report and collection job persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import CollectionJob, Report
from reports.schema import ReportData


class PostgresStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_report(self, tenant_id: str, report: ReportData) -> Report:
        row = Report(tenant_id=tenant_id, **report.__dict__)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def list_reports(self, tenant_id: str, limit: int = 50) -> list[Report]:
        result = await self.db.execute(select(Report).where(Report.tenant_id == tenant_id).order_by(Report.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def get_report(self, tenant_id: str, report_id: str) -> Report | None:
        result = await self.db.execute(select(Report).where(Report.tenant_id == tenant_id, Report.report_id == report_id))
        return result.scalar_one_or_none()

    async def create_job(self, tenant_id: str, target: str, target_type: str) -> CollectionJob:
        job = CollectionJob(tenant_id=tenant_id, target=target, target_type=target_type, status="running")
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def complete_job(self, job: CollectionJob, raw_count: int, enriched_count: int, errors: list[str] | None = None) -> None:
        job.status = "complete" if not errors else "failed"
        job.raw_count = raw_count
        job.enriched_count = enriched_count
        job.errors = errors or []
        job.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
