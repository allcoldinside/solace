import uuid
from datetime import datetime

from sqlalchemy import select

from core.models import ApprovalRequest, Task


class TaskStore:
    def __init__(self, db):
        self.db = db

    async def create_task(self, tenant_id: str, case_id: str, title: str, description: str, priority: str, assigned_to: str, due_at, source_type: str, source_id: str, created_by: str):
        t = Task(task_id=f'TSK-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, case_id=case_id, title=title, description=description, priority=priority, assigned_to=assigned_to, due_at=due_at, source_type=source_type, source_id=source_id, created_by=created_by)
        self.db.add(t); await self.db.commit(); await self.db.refresh(t); return t

    async def get_task(self, tenant_id: str, task_id: str):
        r = await self.db.execute(select(Task).where(Task.tenant_id == tenant_id, Task.task_id == task_id)); return r.scalar_one_or_none()

    async def list_tasks(self, tenant_id: str):
        r = await self.db.execute(select(Task).where(Task.tenant_id == tenant_id)); return list(r.scalars().all())

    async def create_approval(self, tenant_id: str, requested_action: str, target_type: str, target_id: str, requested_by: str, metadata_json: dict):
        a = ApprovalRequest(approval_request_id=f'APR-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, requested_action=requested_action, target_type=target_type, target_id=target_id, requested_by=requested_by, metadata_json=metadata_json)
        self.db.add(a); await self.db.commit(); await self.db.refresh(a); return a

    async def get_approval(self, tenant_id: str, approval_request_id: str):
        r = await self.db.execute(select(ApprovalRequest).where(ApprovalRequest.tenant_id == tenant_id, ApprovalRequest.approval_request_id == approval_request_id)); return r.scalar_one_or_none()

    async def list_approvals(self, tenant_id: str):
        r = await self.db.execute(select(ApprovalRequest).where(ApprovalRequest.tenant_id == tenant_id)); return list(r.scalars().all())
