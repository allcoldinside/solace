from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.models import Report
from core.schemas import ReportGenerateRequest
from reports.structured_generator import build_structured_report
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore
from storage.claim_store import ClaimStore
from storage.entity_store import EntityStore
from storage.timeline_store import TimelineStore

router = APIRouter(prefix='/reports', tags=['reports'])


@router.get('')
async def list_reports(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(Report).where(Report.tenant_id == user.tenant_id))
    return list(r.scalars().all())


@router.get('/{report_id}')
async def get_report(report_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(Report).where(Report.tenant_id == user.tenant_id, Report.report_id == report_id))
    x = r.scalar_one_or_none()
    if not x:
        raise HTTPException(status_code=404, detail='not found')
    return x


@router.post('/cases/{case_id}/generate')
async def generate_case_report(case_id: str, payload: ReportGenerateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    entities = await EntityStore(db).list_by_case(user.tenant_id, case_id)
    timeline = await TimelineStore(db).list_by_case(user.tenant_id, case_id)
    claims = await ClaimStore(db).list_claims(user.tenant_id, case_id)
    evidence_count = 0
    for c in claims:
        evidence_count += len(await ClaimStore(db).list_evidence(user.tenant_id, c.claim_id))

    markdown, payload_json = build_structured_report(payload.title, entities, timeline, claims, evidence_count)

    report = Report(
        report_id=f"RPT-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
        tenant_id=user.tenant_id,
        case_id=case_id,
        title=payload.title,
        report_type=payload.report_type,
        status='generated',
        generated_by=user.user_id,
        content_markdown=markdown,
        content_json=payload_json,
        subject=payload.title,
        subject_type='case',
        classification='TLP:WHITE',
        confidence='MEDIUM',
        confidence_score=payload_json['confidence_score'],
        full_markdown=markdown,
        payload=payload_json,
        updated_at=datetime.utcnow(),
    )
    db.add(report)
    await db.commit(); await db.refresh(report)

    await write_audit(db, user.tenant_id, user.user_id, 'report.generate', 'report', report.report_id, {'case_id': case_id}, request=None)
    return report


@router.get('/{report_id}/export/markdown')
async def export_markdown(report_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(Report).where(Report.tenant_id == user.tenant_id, Report.report_id == report_id))
    report = r.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail='not found')
    return PlainTextResponse(report.content_markdown or report.full_markdown)
