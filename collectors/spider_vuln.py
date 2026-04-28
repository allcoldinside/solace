"""SPIDER-22 vuln intelligence collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from config.settings import get_settings
settings = get_settings()
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderVuln(BaseCollector):
    """Collect vuln intelligence from public and configured sources."""

    bot_id = "SPIDER-22"
    domain = "vuln"

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect source items for the target from vuln endpoints."""
        items = []
        async with aiohttp.ClientSession() as session:
            params = {"q": target}
            headers: dict[str, str] | None = None
            if self.bot_id == "SPIDER-13" and settings.github_token:
                headers = {"Authorization": f"Bearer {settings.github_token}"}
            if self.bot_id == "SPIDER-23" and settings.hibp_api_key:
                headers = {"hibp-api-key": settings.hibp_api_key, "user-agent": "SOLACE-OSINT/1.0"}
                params = {"domain": target}
            payload = await self.fetch_json(session, "https://services.nvd.nist.gov/rest/json/cves/2.0".format(target=target), params=params, headers=headers)
            if payload is not None:
                items.append(self.build_item(source_url="https://services.nvd.nist.gov/rest/json/cves/2.0", source_type="vuln_nvd", content=f"vuln endpoint returned data for {target}.", target=target, target_type=target_type))
        return CollectionResult(collector_id=CollectorID.SPIDER_22, items=items)
