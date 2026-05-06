from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import ClaimCreateRequest, ClaimUpdateRequest
from security.audit import write_audit
from intelligence.timeline_extractor import extract_timeline_candidates
from storage.timeline_store import TimelineStore
from security.deps import current_user
from storage.case_store import CaseStore
from storage.claim_store import ClaimStore

router = APIRouter(prefix='/cases', tags=['claims'])


@router.get('/{case_id}/claims')
async def list_claims(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    return await ClaimStore(db).list_claims(user.tenant_id, case_id)


@router.post('/{case_id}/claims')
async def create_claim(case_id: str, payload: ClaimCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    claim = await ClaimStore(db).create_claim(
        tenant_id=user.tenant_id,
        case_id=case_id,
        document_id=payload.document_id,
        source_id=payload.source_id,
        text=payload.text,
        normalized_text=payload.text.lower().strip(),
        claim_type=payload.claim_type,
        confidence_score=payload.confidence_score,
        verification_status=payload.verification_status.value,
        created_by=user.user_id,
        metadata_json=payload.metadata_json,
    )

    await ClaimStore(db).add_evidence(
        claim_id=claim.claim_id,
        tenant_id=user.tenant_id,
        document_id=payload.document_id,
        source_id=payload.source_id,
        chunk_id='manual',
        start_offset=0,
        end_offset=len(payload.text),
        excerpt_text=payload.text,
    )

    for cand in extract_timeline_candidates(claim.text):
        await TimelineStore(db).create(user.tenant_id, case_id, cand['event_time'], cand['title'], cand['description'], claim.source_id, claim.claim_id, claim.confidence_score, {'generated_from_claim': True})

    await write_audit(db, user.tenant_id, user.user_id, 'claim.create', 'claim', claim.claim_id, {'case_id': case_id}, request=request)
    return claim


@router.patch('/claims/{claim_id}')
async def update_claim(claim_id: str, payload: ClaimUpdateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    claim = await ClaimStore(db).get_claim(user.tenant_id, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail='claim not found')
    updates = payload.model_dump(exclude_none=True)
    for key, value in updates.items():
        setattr(claim, key, value.value if hasattr(value, 'value') else value)
    await db.commit()
    await db.refresh(claim)
    await write_audit(db, user.tenant_id, user.user_id, 'claim.update', 'claim', claim_id, {'updates': updates}, request=request)
    return claim


@router.get('/claims/{claim_id}/evidence')
async def claim_evidence(claim_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    claim = await ClaimStore(db).get_claim(user.tenant_id, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail='claim not found')
    return await ClaimStore(db).list_evidence(user.tenant_id, claim_id)
