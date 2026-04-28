"""MISP client integration for IOC sharing."""

from __future__ import annotations

import aiohttp

from config.settings import get_settings
settings = get_settings()
from reports.schema import ReportData


class MISPClient:
    """Perform IOC push/pull operations against a MISP instance."""

    def __init__(self) -> None:
        """Initialize static MISP headers."""
        self._headers = {
            "Authorization": settings.misp_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def push_iocs(self, report_id: str, iocs: list[dict[str, str]]) -> str:
        """Create a MISP event for IOC list and return event identifier."""
        payload = {"Event": {"info": f"SOLACE report {report_id}", "Attribute": iocs}}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.misp_url}/events", json=payload, headers=self._headers, timeout=20) as response:
                data = await response.json(content_type=None)
                event = data.get("Event", {}) if isinstance(data, dict) else {}
                return str(event.get("id", ""))

    async def pull_threat_intel(self, target: str) -> list[dict[str, str]]:
        """Search MISP attributes by value and return attribute results."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.misp_url}/attributes/restSearch", params={"value": target}, headers=self._headers, timeout=20) as response:
                data = await response.json(content_type=None)
                if isinstance(data, dict):
                    return list(data.get("response", {}).get("Attribute", []))
                return []

    async def create_event(self, report: ReportData) -> str:
        """Create full report-based MISP event and return event identifier."""
        attributes = [{"type": "comment", "value": finding} for finding in report.key_findings]
        return await self.push_iocs(report.report_id, attributes)
