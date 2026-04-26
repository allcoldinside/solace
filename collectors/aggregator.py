"""Collector aggregation and normalization logic."""

from __future__ import annotations

from core.schemas import CollectionResult, RawIntelItemSchema

SOURCE_RELIABILITY: dict[str, float] = {"seed": 0.75, "news": 0.7, "official": 0.95}


class AggregatorBot:
    def process(self, results: list[CollectionResult]) -> list[RawIntelItemSchema]:
        unique: dict[str, RawIntelItemSchema] = {}
        for result in results:
            for item in result.items:
                if len(item.content.strip()) < 40:
                    continue
                score = SOURCE_RELIABILITY.get(item.source_type, item.reliability_score)
                unique[item.content_hash] = item.model_copy(update={"reliability_score": max(0.0, min(1.0, score))})
        return sorted(unique.values(), key=lambda item: item.reliability_score, reverse=True)
