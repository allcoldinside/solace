import uuid

from sqlalchemy import select

from core.models import AgentResponse, PanelRun


class PanelRunStore:
    def __init__(self, db):
        self.db = db

    async def create_run(self, tenant_id: str, case_id: str, report_id: str, prompt: str, consensus_summary: str, created_by: str):
        run = PanelRun(panel_run_id=f'PRN-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, case_id=case_id, report_id=report_id, prompt=prompt, consensus_summary=consensus_summary, created_by=created_by, status='completed')
        self.db.add(run); await self.db.commit(); await self.db.refresh(run); return run

    async def add_response(self, panel_run_id: str, agent_role: str, response_text: str, confidence_score: float, concerns_json: dict):
        r = AgentResponse(agent_response_id=f'ARSP-{uuid.uuid4().hex[:10]}', panel_run_id=panel_run_id, agent_role=agent_role, response_text=response_text, confidence_score=confidence_score, concerns_json=concerns_json)
        self.db.add(r); await self.db.commit(); await self.db.refresh(r); return r

    async def get_run(self, tenant_id: str, panel_run_id: str):
        r = await self.db.execute(select(PanelRun).where(PanelRun.tenant_id == tenant_id, PanelRun.panel_run_id == panel_run_id))
        return r.scalar_one_or_none()

    async def list_runs(self, tenant_id: str, case_id: str):
        r = await self.db.execute(select(PanelRun).where(PanelRun.tenant_id == tenant_id, PanelRun.case_id == case_id))
        return list(r.scalars().all())

    async def list_responses(self, panel_run_id: str):
        r = await self.db.execute(select(AgentResponse).where(AgentResponse.panel_run_id == panel_run_id))
        return list(r.scalars().all())
