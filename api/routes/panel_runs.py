from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import PanelApproveRequest, PanelRunCreateRequest
from panel.provider import MockPanelProvider
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore
from storage.claim_store import ClaimStore
from storage.panel_run_store import PanelRunStore
from storage.task_store import TaskStore

router = APIRouter(prefix='/cases', tags=['panel-runs'])


@router.post('/{case_id}/panel-runs')
async def start_panel_run(case_id: str, payload: PanelRunCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    claims = await ClaimStore(db).list_claims(user.tenant_id, case_id)
    claim_dicts = [{'claim_id': c.claim_id, 'text': c.text} for c in claims]
    evidence_count = 0
    for c in claims:
        evidence_count += len(await ClaimStore(db).list_evidence(user.tenant_id, c.claim_id))

    provider = MockPanelProvider()
    responses = provider.run(payload.prompt, claim_dicts, evidence_count)
    consensus = 'Consensus is evidence-constrained. Human approval required before task conversion.'

    store = PanelRunStore(db)
    run = await store.create_run(user.tenant_id, case_id, payload.report_id, payload.prompt, consensus, user.user_id)
    for r in responses:
        await store.add_response(run.panel_run_id, r['agent_role'], r['response_text'], r['confidence_score'], r['concerns_json'])

    await write_audit(db, user.tenant_id, user.user_id, 'panel_run.create', 'panel_run', run.panel_run_id, {'case_id': case_id}, request=request)
    return run


@router.get('/{case_id}/panel-runs')
async def list_panel_runs(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    return await PanelRunStore(db).list_runs(user.tenant_id, case_id)


@router.get('/panel-runs/{panel_run_id}/responses')
async def list_panel_responses(panel_run_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    run = await PanelRunStore(db).get_run(user.tenant_id, panel_run_id)
    if not run:
        raise HTTPException(status_code=404, detail='panel run not found')
    return await PanelRunStore(db).list_responses(panel_run_id)


@router.post('/panel-runs/{panel_run_id}/approve')
async def approve_panel_run(panel_run_id: str, payload: PanelApproveRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    run = await PanelRunStore(db).get_run(user.tenant_id, panel_run_id)
    if not run:
        raise HTTPException(status_code=404, detail='panel run not found')
    run.status = 'approved' if payload.approved else 'rejected'
    await db.commit(); await db.refresh(run)
    await write_audit(db, user.tenant_id, user.user_id, 'panel_run.approve', 'panel_run', panel_run_id, {'approved': payload.approved}, request=request)
    return run


@router.post('/panel-runs/{panel_run_id}/convert-to-tasks')
async def convert_panel_to_tasks(panel_run_id: str, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    run = await PanelRunStore(db).get_run(user.tenant_id, panel_run_id)
    if not run:
        raise HTTPException(status_code=404, detail='panel run not found')

    approval = await TaskStore(db).create_approval(
        tenant_id=user.tenant_id,
        requested_action='create_task',
        target_type='panel_run',
        target_id=panel_run_id,
        requested_by=user.user_id,
        metadata_json={
            'case_id': run.case_id,
            'title': f'Panel Recommendation for {run.case_id}',
            'description': run.consensus_summary,
            'priority': 'medium',
            'assigned_to': '',
        },
    )
    await write_audit(db, user.tenant_id, user.user_id, 'panel_run.request_task_approval', 'approval_request', approval.approval_request_id, {'panel_run_id': panel_run_id}, request=request)
    return approval
