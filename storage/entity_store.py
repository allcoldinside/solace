import uuid

from sqlalchemy import select

from core.models import Entity, EntityRelationship


class EntityStore:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def _normalize(name: str) -> str:
        return ' '.join(name.lower().split())

    async def upsert(
        self,
        tenant_id: str,
        case_id: str,
        canonical_name: str,
        entity_type: str,
        confidence_score: float = 0.5,
        aliases: list[str] | None = None,
        metadata_json: dict | None = None,
    ):
        normalized = self._normalize(canonical_name)
        r = await self.db.execute(
            select(Entity).where(Entity.tenant_id == tenant_id, Entity.case_id == case_id)
        )
        existing = None
        for e in r.scalars().all():
            names = [e.canonical_name] + (e.aliases or [])
            if normalized in {self._normalize(n) for n in names}:
                existing = e
                break

        if existing:
            alias_set = set(existing.aliases or [])
            alias_set.update(aliases or [])
            existing.aliases = sorted(alias_set)
            existing.confidence_score = max(existing.confidence_score, confidence_score)
            existing.metadata_json = {**(existing.metadata_json or {}), **(metadata_json or {})}
            entity = existing
        else:
            entity = Entity(
                entity_id=f'ENTITY-{uuid.uuid4().hex[:10]}',
                tenant_id=tenant_id,
                case_id=case_id,
                entity_type=entity_type,
                canonical_name=canonical_name,
                aliases=aliases or [],
                confidence_score=confidence_score,
                metadata_json=metadata_json or {},
            )
            self.db.add(entity)

        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def list_by_case(self, tenant_id: str, case_id: str):
        r = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.case_id == case_id))
        return list(r.scalars().all())

    async def merge(self, tenant_id: str, primary_entity_id: str, duplicate_entity_id: str):
        p = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.entity_id == primary_entity_id))
        d = await self.db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.entity_id == duplicate_entity_id))
        primary = p.scalar_one_or_none(); duplicate = d.scalar_one_or_none()
        if not primary or not duplicate:
            return None
        aliases = set(primary.aliases or [])
        aliases.add(duplicate.canonical_name)
        aliases.update(duplicate.aliases or [])
        primary.aliases = sorted(aliases)
        await self.db.delete(duplicate)
        await self.db.commit()
        await self.db.refresh(primary)
        return primary


class RelationshipStore:
    def __init__(self, db):
        self.db = db

    async def create(self, tenant_id: str, case_id: str, subject_entity_id: str, predicate: str, object_entity_id: str, source_id: str, claim_id: str, confidence_score: float = 0.5, metadata_json: dict | None = None):
        rel = EntityRelationship(
            relationship_id=f'REL-{uuid.uuid4().hex[:10]}',
            tenant_id=tenant_id,
            case_id=case_id,
            subject_entity_id=subject_entity_id,
            predicate=predicate,
            object_entity_id=object_entity_id,
            source_id=source_id,
            claim_id=claim_id,
            confidence_score=confidence_score,
            metadata_json=metadata_json or {},
        )
        self.db.add(rel)
        await self.db.commit(); await self.db.refresh(rel)
        return rel

    async def list_by_case(self, tenant_id: str, case_id: str):
        r = await self.db.execute(select(EntityRelationship).where(EntityRelationship.tenant_id == tenant_id, EntityRelationship.case_id == case_id))
        return list(r.scalars().all())
