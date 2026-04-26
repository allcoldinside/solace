"""Basic entity extraction and normalization."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

ENTITY_RE = re.compile(r"\b(?:[A-Z][a-zA-Z0-9&.-]+(?:\s+[A-Z][a-zA-Z0-9&.-]+){0,4})\b")
ORG_HINTS = ("Inc", "LLC", "Corp", "Corporation", "Company", "Group", "Labs", "Systems", "University", "Agency")


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).lower()


def classify_entity(name: str) -> str:
    if any(hint.lower() in name.lower() for hint in ORG_HINTS):
        return "organization"
    if re.search(r"\b(?:Florida|London|Paris|Tokyo|Central Florida)\b", name):
        return "location"
    return "person_or_named_object"


class EntityResolver:
    def extract(self, enriched_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, str], dict[str, Any]] = {}
        for item in enriched_items:
            candidates = set(item.get("candidate_entities") or [])
            candidates.update(match.group(0) for match in ENTITY_RE.finditer(item.get("content", "")))
            for name in candidates:
                clean = name.strip(" .,-")
                if len(clean) < 3 or clean.lower() in {"seed", "target", "type", "this", "local"}:
                    continue
                entity_type = classify_entity(clean)
                key = (normalize_name(clean), entity_type)
                current = grouped.setdefault(key, {"name": clean, "normalized_name": key[0], "entity_type": entity_type, "confidence_score": 0.55, "attributes": {"mentions": 0}, "source_report_ids": []})
                current["attributes"]["mentions"] += 1
                current["confidence_score"] = min(0.95, current["confidence_score"] + 0.05)
        return list(grouped.values())


async def resolve_entities(enriched_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return EntityResolver().extract(enriched_items)
