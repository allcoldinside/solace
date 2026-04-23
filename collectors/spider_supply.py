"""SPIDER-17 supply intelligence collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from config.settings import settings
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderSupply(BaseCollector):
    """Collect supply intelligence from public and configured sources."""

    bot_id = "SPIDER-17"
    domain = "supply"

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect source items for the target from supply endpoints."""
        items = []
        async with aiohttp.ClientSession() as session:
            params = {"q": target}
            headers: dict[str, str] | None = None
            if self.bot_id == "SPIDER-13" and settings.github_token:
                headers = {"Authorization": f"Bearer {settings.github_token}"}
            if self.bot_id == "SPIDER-23" and settings.hibp_api_key:
                headers = {"hibp-api-key": settings.hibp_api_key, "user-agent": "SOLACE-OSINT/1.0"}
                params = {"domain": target}
            payload = await self.fetch_json(session, "https://search.worldbank.org/api/v2/procurement".format(target=target), params=params, headers=headers)
            if payload is not None:
                items.append(self.build_item(source_url="https://search.worldbank.org/api/v2/procurement", source_type="supply_worldbank", content=f"supply endpoint returned data for {target}.", target=target, target_type=target_type))
        return CollectionResult(collector_id=CollectorID.SPIDER_17, items=items)
