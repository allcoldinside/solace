"""Replaceable graph ingest stub."""

from __future__ import annotations

from typing import Any


class GraphBuilder:
    async def ingest(self, tenant_id: str, report_id: str, entities: list[dict[str, Any]]) -> dict[str, Any]:
        nodes = [{"id": item.get("entity_id") or item.get("normalized_name"), "label": item.get("name"), "type": item.get("entity_type")} for item in entities]
        return {"tenant_id": tenant_id, "report_id": report_id, "nodes": nodes, "edges": []}
