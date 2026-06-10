from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import TimelineEntryCreateRequest
from intelligence.timeline_extractor import extract_timeline_candidates
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore
from storage.claim_store import ClaimStore
from storage.timeline_store import TimelineStore

router = APIRouter(prefix='/cases', tags=['timeline'])


@router.get('/{case_id}/timeline')
async def list_timeline(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    return await TimelineStore(db).list_by_case(user.tenant_id, case_id)


@router.post('/{case_id}/timeline')
async def create_timeline_entry(case_id: str, payload: TimelineEntryCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    entry = await TimelineStore(db).create(
        tenant_id=user.tenant_id,
        case_id=case_id,
        event_time=payload.event_time,
        title=payload.title,
        description=payload.description,
        source_id=payload.source_id,
        claim_id=payload.claim_id,
        confidence_score=payload.confidence_score,
        metadata_json=payload.metadata_json,
    )
    await write_audit(db, user.tenant_id, user.user_id, 'timeline.create', 'timeline_entry', entry.timeline_entry_id, {'case_id': case_id}, request=request)
    return entry


@router.post('/{case_id}/timeline/generate')
async def generate_timeline(case_id: str, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    claims = await ClaimStore(db).list_claims(user.tenant_id, case_id)
    created = []
    for claim in claims:
        for cand in extract_timeline_candidates(claim.text):
            entry = await TimelineStore(db).create(
                tenant_id=user.tenant_id,
                case_id=case_id,
                event_time=cand['event_time'],
                title=cand['title'],
                description=cand['description'],
                source_id=claim.source_id,
                claim_id=claim.claim_id,
                confidence_score=claim.confidence_score,
                metadata_json={'generated_from_claim': True},
            )
            created.append(entry)
    await write_audit(db, user.tenant_id, user.user_id, 'timeline.generate', 'timeline_entry', case_id, {'count': len(created)}, request=request)
    return {'created': len(created)}
