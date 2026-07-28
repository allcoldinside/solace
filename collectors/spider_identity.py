"""SPIDER-9 identity intelligence collector."""

from __future__ import annotations

import asyncio

import aiohttp

from collectors.base import BaseCollector
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderIdentity(BaseCollector):
    """Collect identity indicators from username and account footprint sources."""

    bot_id = "SPIDER-9"
    domain = "identity"
    source_reliability = 0.72

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect identity profile hints for a target string."""
        items = []
        async with aiohttp.ClientSession() as session:
            data = await self.fetch_json(
                session,
                "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json",
            )
            if isinstance(data, dict):
                checks = data.get("sites", [])[:20]
                sem = asyncio.Semaphore(20)

                async def check_site(site: dict[str, str]) -> None:
                    uri_check = str(site.get("uri_check", "")).replace("{account}", target)
                    if not uri_check:
                        return
                    async with sem:
                        try:
                            async with session.head(uri_check, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                if response.status < 400:
                                    items.append(
                                        self.build_item(
                                            source_url=uri_check,
                                            source_type="wmn_username",
                                            content=f"Possible username presence for {target} on {site.get('name', 'unknown')} ({response.status}).",
                                            target=target,
                                            target_type=target_type,
                                        )
                                    )
                        except aiohttp.ClientError:
                            return

                await asyncio.gather(*(check_site(entry) for entry in checks))
        return CollectionResult(collector_id=CollectorID.SPIDER_9, items=items)
