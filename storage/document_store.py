import uuid

from sqlalchemy import select

from core.models import Document


class DocumentStore:
    def __init__(self, db):
        self.db = db

    async def create(
        self,
        tenant_id: str,
        case_id: str,
        source_id: str,
        title: str,
        mime_type: str,
        object_key: str,
        sha256_hash: str,
        size_bytes: int,
        text_content: str,
    ) -> Document:
        document = Document(
            document_id=f'DOC-{uuid.uuid4().hex[:10]}',
            tenant_id=tenant_id,
            case_id=case_id,
            source_id=source_id,
            title=title,
            mime_type=mime_type,
            object_key=object_key,
            sha256_hash=sha256_hash,
            size_bytes=size_bytes,
            text_content=text_content,
        )
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def find_by_hash(self, tenant_id: str, case_id: str, sha256_hash: str):
        q = select(Document).where(
            Document.tenant_id == tenant_id,
            Document.case_id == case_id,
            Document.sha256_hash == sha256_hash,
        )
        r = await self.db.execute(q)
        return r.scalar_one_or_none()
