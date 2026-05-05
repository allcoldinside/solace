"""Full-text search engine over reports, entities, and cases."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Case, Entity, Report
from core.schemas import SearchResultSchema


class SearchEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def query(self, tenant_id: str, q: str, limit: int = 20) -> list[SearchResultSchema]:
        if not q or not q.strip():
            return []
        term = f"%{q.strip()}%"
        results: list[SearchResultSchema] = []

        report_rows = await self.db.execute(
            select(Report)
            .where(
                Report.tenant_id == tenant_id,
                or_(Report.subject.ilike(term), Report.executive_summary.ilike(term)),
            )
            .limit(limit)
        )
        for row in report_rows.scalars().all():
            snippet = (row.executive_summary or "")[:120].replace("\n", " ")
            results.append(SearchResultSchema(id=row.report_id, type="report", title=row.subject, snippet=snippet, score=1.0))

        entity_rows = await self.db.execute(
            select(Entity)
            .where(Entity.tenant_id == tenant_id, Entity.name.ilike(term))
            .limit(limit)
        )
        for row in entity_rows.scalars().all():
            results.append(SearchResultSchema(id=row.entity_id, type="entity", title=row.name, snippet=row.entity_type, score=0.9))

        case_rows = await self.db.execute(
            select(Case)
            .where(Case.tenant_id == tenant_id, or_(Case.title.ilike(term), Case.description.ilike(term)))
            .limit(limit)
        )
        for row in case_rows.scalars().all():
            results.append(SearchResultSchema(id=row.case_id, type="case", title=row.title, snippet=(row.description or "")[:120], score=0.8))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]
