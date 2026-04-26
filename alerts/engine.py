"""Alert routing stub."""

from __future__ import annotations

from reports.schema import ReportData


class AlertEngine:
    async def evaluate(self, report: ReportData) -> dict:
        route = "log"
        if report.classification == "TLP:RED":
            route = "priority"
        elif report.classification == "TLP:AMBER":
            route = "standard"
        return {"alerted": False, "route": route, "reason": "external alert integrations are not configured"}
