"""Deterministic seed collector for local/offline pipeline runs."""

from __future__ import annotations

from core.schemas import CollectionResult, TargetType
from collectors.base_collector import BaseCollector


class SeedCollector(BaseCollector):
    collector_id = "SEED"

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        body = (
            f"Seed intelligence packet for {target}. "
            f"Target type: {target_type.value}. "
            "This local source proves SOLACE collection, enrichment, entity resolution, reporting, memory, panel, and alert flow without external APIs. "
            f"Organization hint: {target} Operations Group. Location hint: Central Florida."
        )
        return self._build_result([
            self._build_item(
                source_url="seed://local/bootstrap",
                source_type="seed",
                content=body,
                target=target,
                target_type=target_type,
                reliability_score=0.75,
                metadata_={"offline": True},
            )
        ])
