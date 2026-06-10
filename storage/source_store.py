import uuid
from datetime import datetime

from sqlalchemy import select

from core.models import Source


class SourceStore:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        tenant_id: str,
        case_id: str,
        source_type: str,
        name: str,
        uri: str,
        collection_method: str,
        authorization_basis: str,
        collected_by: str,
        metadata_json: dict,
    ) -> Source:
        source = Source(
            source_id=f'SRC-{uuid.uuid4().hex[:10]}',
            tenant_id=tenant_id,
            case_id=case_id,
            source_type=source_type,
            name=name,
            uri=uri,
            collection_method=collection_method,
            authorization_basis=authorization_basis,
            collected_at=datetime.utcnow(),
            collected_by=collected_by,
            metadata_json=metadata_json,
        )
        self.db.add(source)
        await self.db.commit()
        await self.db.refresh(source)
        return source

    async def get(self, tenant_id: str, source_id: str):
        q = select(Source).where(Source.tenant_id == tenant_id, Source.source_id == source_id)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()
