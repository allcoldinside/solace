"""Audit log persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AuditLog


class AuditStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, tenant_id: str, limit: int = 100) -> list[AuditLog]:
        result = await self.db.execute(select(AuditLog).where(AuditLog.tenant_id == tenant_id).order_by(AuditLog.created_at.desc()).limit(limit))
        return list(result.scalars().all())
