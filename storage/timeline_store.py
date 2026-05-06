import uuid
from datetime import datetime

from sqlalchemy import select

from core.models import TimelineEntry


class TimelineStore:
    def __init__(self, db):
        self.db = db

    async def create(self, tenant_id: str, case_id: str, event_time: datetime, title: str, description: str, source_id: str, claim_id: str, confidence_score: float, metadata_json: dict):
        entry = TimelineEntry(
            timeline_entry_id=f'TLE-{uuid.uuid4().hex[:10]}',
            tenant_id=tenant_id,
            case_id=case_id,
            event_time=event_time,
            title=title,
            description=description,
            source_id=source_id,
            claim_id=claim_id,
            confidence_score=confidence_score,
            metadata_json=metadata_json,
        )
        self.db.add(entry)
        await self.db.commit(); await self.db.refresh(entry)
        return entry

    async def list_by_case(self, tenant_id: str, case_id: str):
        r = await self.db.execute(
            select(TimelineEntry)
            .where(TimelineEntry.tenant_id == tenant_id, TimelineEntry.case_id == case_id)
            .order_by(TimelineEntry.event_time.asc())
        )
        return list(r.scalars().all())
