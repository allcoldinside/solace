from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import ApprovalDecisionRequest, TaskCreateRequest, TaskUpdateRequest
from security.audit import write_audit
from security.deps import current_user
from storage.task_store import TaskStore

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('')
async def create_task(payload: TaskCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    task = await TaskStore(db).create_task(user.tenant_id, payload.case_id, payload.title, payload.description, payload.priority, payload.assigned_to, payload.due_at, payload.source_type, payload.source_id, user.user_id)
    await write_audit(db, user.tenant_id, user.user_id, 'task.create', 'task', task.task_id, {'case_id': payload.case_id}, request=request)
    return task


@router.patch('/{task_id}')
async def update_task(task_id: str, payload: TaskUpdateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    task = await TaskStore(db).get_task(user.tenant_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='task not found')
    updates = payload.model_dump(exclude_none=True)
    for k, v in updates.items():
        setattr(task, k, v)
    await db.commit(); await db.refresh(task)
    await write_audit(db, user.tenant_id, user.user_id, 'task.update', 'task', task_id, {'updates': updates}, request=request)
    return task


@router.get('')
async def list_tasks(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await TaskStore(db).list_tasks(user.tenant_id)


@router.get('/approvals')
async def list_approvals(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await TaskStore(db).list_approvals(user.tenant_id)


@router.post('/approvals/{approval_request_id}/decision')
async def decision_approval(approval_request_id: str, payload: ApprovalDecisionRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    if payload.status not in {'approved', 'rejected', 'cancelled'}:
        raise HTTPException(status_code=400, detail='invalid status')
    approval = await TaskStore(db).get_approval(user.tenant_id, approval_request_id)
    if not approval:
        raise HTTPException(status_code=404, detail='approval request not found')

    approval.status = payload.status
    approval.approved_by = user.user_id
    approval.resolved_at = datetime.utcnow()

    created_task = None
    if payload.status == 'approved' and approval.requested_action == 'create_task':
        meta = approval.metadata_json
        created_task = await TaskStore(db).create_task(
            user.tenant_id,
            meta.get('case_id', ''),
            meta.get('title', 'Panel Recommendation'),
            meta.get('description', ''),
            meta.get('priority', 'medium'),
            meta.get('assigned_to', ''),
            None,
            'panel_recommendation',
            approval.target_id,
            approval.requested_by,
        )

    await db.commit(); await db.refresh(approval)
    await write_audit(db, user.tenant_id, user.user_id, 'approval.decision', 'approval_request', approval_request_id, {'status': payload.status, 'created_task_id': getattr(created_task, 'task_id', '')}, request=request)
    return {'approval': approval, 'created_task': created_task}
