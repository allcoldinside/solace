from core.models import MemoryEntry


async def save_memory(db, tenant_id: str, report_id: str, content: str, meta: dict):
    m = MemoryEntry(tenant_id=tenant_id, report_id=report_id, content=content, meta=meta)
    db.add(m); await db.commit(); return m
