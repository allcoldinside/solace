"""Lightweight enrichment pipeline with no external model dependency."""

from __future__ import annotations

import re
from typing import Any

from core.schemas import RawIntelItemSchema

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9&.\-]{2,}")


async def enrich_items(items: list[RawIntelItemSchema]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for item in items:
        words = WORD_RE.findall(item.content)
        keywords = sorted({w.lower().strip(".") for w in words if len(w) > 4})[:20]
        entities = [w.strip(".") for w in words if w[:1].isupper()][:25]
        enriched.append({
            "content_hash": item.content_hash,
            "collector_id": str(item.collector_id),
            "source_url": item.source_url,
            "source_type": item.source_type,
            "content": item.content,
            "target": item.target,
            "target_type": item.target_type.value,
            "reliability_score": item.reliability_score,
            "keywords": keywords,
            "candidate_entities": entities,
            "language": "en",
            "sentiment": 0.0,
        })
    return enriched
