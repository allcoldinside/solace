import uuid

from core.models import DocumentChunk


class ChunkStore:
    def __init__(self, db):
        self.db = db

    async def replace_for_document(self, tenant_id: str, document_id: str, chunks: list[dict]):
        await self.db.execute(DocumentChunk.__table__.delete().where(DocumentChunk.document_id == document_id))
        created = []
        for c in chunks:
            chunk_id = f"CHK-{uuid.uuid4().hex[:10]}"
            self.db.add(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    tenant_id=tenant_id,
                    chunk_index=c['chunk_index'],
                    start_offset=c['start_offset'],
                    end_offset=c['end_offset'],
                    text=c['text'],
                )
            )
            created.append({**c, 'chunk_id': chunk_id})
        await self.db.commit()
        return created
