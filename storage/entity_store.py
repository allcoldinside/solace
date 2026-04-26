"""Tenant-aware entity persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Entity


class EntityStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_many(self, tenant_id: str, entities: list[dict[str, Any]], report_id: str | None = None) -> list[Entity]:
        saved: list[Entity] = []
        for item in entities:
            normalized = item["normalized_name"]
            entity_type = item["entity_type"]
            result = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.normalized_name == normalized, Entity.entity_type == entity_type))
            row = result.scalar_one_or_none()
            if row is None:
                row = Entity(tenant_id=tenant_id, **item)
                self.db.add(row)
            else:
                row.confidence_score = max(row.confidence_score, float(item.get("confidence_score", 0.5)))
                row.attributes = {**(row.attributes or {}), **item.get("attributes", {})}
                row.updated_at = datetime.now(timezone.utc)
            if report_id and report_id not in (row.source_report_ids or []):
                row.source_report_ids = [*(row.source_report_ids or []), report_id]
            saved.append(row)
        await self.db.commit()
        for row in saved:
            await self.db.refresh(row)
        return saved

    async def list(self, tenant_id: str, limit: int = 100) -> list[Entity]:
        result = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id).order_by(Entity.created_at.desc()).limit(limit))
        return list(result.scalars().all())
