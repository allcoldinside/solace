import uuid
from sqlalchemy import select
from core.models import Entity


class EntityStore:
    def __init__(self, db): self.db = db

    async def upsert(self, tenant_id: str, name: str, kind: str, confidence: float = 0.5, attributes: dict | None = None):
        r = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.name == name, Entity.kind == kind))
        e = r.scalar_one_or_none()
        if e:
            e.confidence = max(e.confidence, confidence)
            e.attributes = {**(e.attributes or {}), **(attributes or {})}
        else:
            e = Entity(entity_id=f'ENTITY-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, name=name, kind=kind, confidence=confidence, attributes=attributes or {})
            self.db.add(e)
        await self.db.commit(); await self.db.refresh(e)
        return e

    async def list(self, tenant_id: str):
        r = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id)); return list(r.scalars().all())
