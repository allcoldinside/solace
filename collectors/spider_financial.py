"""SPIDER-16 financial intelligence collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from config.settings import settings
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderFinancial(BaseCollector):
    """Collect financial intelligence from public and configured sources."""

    bot_id = "SPIDER-16"
    domain = "financial"

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect source items for the target from financial endpoints."""
        items = []
        async with aiohttp.ClientSession() as session:
            params = {"q": target}
            headers: dict[str, str] | None = None
            if self.bot_id == "SPIDER-13" and settings.github_token:
                headers = {"Authorization": f"Bearer {settings.github_token}"}
            if self.bot_id == "SPIDER-23" and settings.hibp_api_key:
                headers = {"hibp-api-key": settings.hibp_api_key, "user-agent": "SOLACE-OSINT/1.0"}
                params = {"domain": target}
            payload = await self.fetch_json(session, "https://api.coingecko.com/api/v3/search".format(target=target), params=params, headers=headers)
            if payload is not None:
                items.append(self.build_item(source_url="https://api.coingecko.com/api/v3/search", source_type="crypto_coingecko", content=f"financial endpoint returned data for {target}.", target=target, target_type=target_type))
        return CollectionResult(collector_id=CollectorID.SPIDER_16, items=items)
