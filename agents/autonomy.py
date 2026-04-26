"""Autonomous task generation."""

from __future__ import annotations

from typing import Any

from core.models import AutonomousTask
from reports.schema import ReportData


class AutonomyEngine:
    def __init__(self, db: Any | None = None):
        self.db = db

    async def generate_tasks(self, tenant_id: str, report: ReportData) -> list[dict[str, Any]]:
        tasks = [
            {"tenant_id": tenant_id, "report_id": report.report_id, "title": f"Validate sources for {report.subject}", "description": "Review source log and configure higher-fidelity collectors.", "priority": "default"},
            {"tenant_id": tenant_id, "report_id": report.report_id, "title": f"Close intelligence gaps for {report.subject}", "description": "Assign follow-on collection requirements from the report gaps section.", "priority": "high" if report.confidence == "LOW" else "default"},
        ]
        if self.db is not None:
            self.db.add_all([AutonomousTask(**task) for task in tasks])
            await self.db.commit()
        return tasks
