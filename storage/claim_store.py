import uuid

from sqlalchemy import select

from core.models import Claim, EvidenceItem


class ClaimStore:
    def __init__(self, db):
        self.db = db

    async def create_claim(
        self,
        tenant_id: str,
        case_id: str,
        document_id: str,
        source_id: str,
        text: str,
        normalized_text: str,
        claim_type: str,
        confidence_score: float,
        verification_status: str,
        created_by: str,
        metadata_json: dict,
    ) -> Claim:
        claim = Claim(
            claim_id=f'CLM-{uuid.uuid4().hex[:10]}',
            tenant_id=tenant_id,
            case_id=case_id,
            document_id=document_id,
            source_id=source_id,
            text=text,
            normalized_text=normalized_text,
            claim_type=claim_type,
            confidence_score=confidence_score,
            verification_status=verification_status,
            created_by=created_by,
            metadata_json=metadata_json,
        )
        self.db.add(claim)
        await self.db.commit()
        await self.db.refresh(claim)
        return claim

    async def list_claims(self, tenant_id: str, case_id: str):
        r = await self.db.execute(select(Claim).where(Claim.tenant_id == tenant_id, Claim.case_id == case_id))
        return list(r.scalars().all())

    async def get_claim(self, tenant_id: str, claim_id: str):
        r = await self.db.execute(select(Claim).where(Claim.tenant_id == tenant_id, Claim.claim_id == claim_id))
        return r.scalar_one_or_none()

    async def add_evidence(
        self,
        claim_id: str,
        tenant_id: str,
        document_id: str,
        source_id: str,
        chunk_id: str,
        start_offset: int,
        end_offset: int,
        excerpt_text: str,
    ) -> EvidenceItem:
        evidence = EvidenceItem(
            evidence_id=f'EVI-{uuid.uuid4().hex[:10]}',
            claim_id=claim_id,
            tenant_id=tenant_id,
            document_id=document_id,
            source_id=source_id,
            chunk_id=chunk_id,
            start_offset=start_offset,
            end_offset=end_offset,
            excerpt_text=excerpt_text,
        )
        self.db.add(evidence)
        await self.db.commit()
        await self.db.refresh(evidence)
        return evidence

    async def list_evidence(self, tenant_id: str, claim_id: str):
        r = await self.db.execute(select(EvidenceItem).where(EvidenceItem.tenant_id == tenant_id, EvidenceItem.claim_id == claim_id))
        return list(r.scalars().all())
