"""Panel session persistence."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import PanelSessionRecord


class PanelStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, payload: dict[str, Any]) -> PanelSessionRecord:
        row = PanelSessionRecord(**payload)
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def list(self, tenant_id: str) -> list[PanelSessionRecord]:
        result = await self.db.execute(select(PanelSessionRecord).where(PanelSessionRecord.tenant_id == tenant_id).order_by(PanelSessionRecord.created_at.desc()))
        return list(result.scalars().all())

    async def get(self, tenant_id: str, session_id: str) -> PanelSessionRecord | None:
        result = await self.db.execute(select(PanelSessionRecord).where(PanelSessionRecord.tenant_id == tenant_id, PanelSessionRecord.session_id == session_id))
        return result.scalar_one_or_none()
