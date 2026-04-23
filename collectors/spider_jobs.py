"""SPIDER-11 job listings intelligence collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderJobs(BaseCollector):
    """Collect hiring and role trend intelligence from job platforms."""

    bot_id = "SPIDER-11"
    domain = "jobs"
    source_reliability = 0.70

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect public job listing snippets for a target entity."""
        items = []
        async with aiohttp.ClientSession() as session:
            indeed_html = await self.fetch_text(session, "https://www.indeed.com/jobs", params={"q": target, "sort": "date"})
            if indeed_html:
                items.append(self.build_item(source_url="https://www.indeed.com/jobs", source_type="job_listing_indeed", content=f"Indeed listings mention target {target}; page size {len(indeed_html)} chars.", target=target, target_type=target_type))
            remote = await self.fetch_json(session, "https://remoteok.com/api", params={"tag": target})
            if isinstance(remote, list) and remote:
                items.append(self.build_item(source_url="https://remoteok.com/api", source_type="job_listing_remote", content=f"RemoteOK returned {max(0, len(remote)-1)} candidate postings for tag {target}.", target=target, target_type=target_type))
        return CollectionResult(collector_id=CollectorID.SPIDER_11, items=items)
