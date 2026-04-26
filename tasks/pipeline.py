"""Canonical SOLACE pipeline."""

from __future__ import annotations

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import PipelineRequest, PipelineResponse
from collectors.seed_collector import SeedCollector
from collectors.aggregator import AggregatorBot
from nlp.pipeline import enrich_items
from reports.generator import generate_report
from core.invariants import validate_report


async def run_pipeline(db: AsyncSession, request: PipelineRequest, user: Any | None = None) -> PipelineResponse:
    collected = await SeedCollector().collect(request.target, request.target_type)
    raw_items = AggregatorBot().process([collected])
    enriched = await enrich_items(raw_items)
    names = []
    for item in enriched:
        names.extend(item.get("candidate_entities", [])[:5])
    report = generate_report(request.target, request.target_type.value, enriched, {"candidates": names})
    validate_report(report)
    return PipelineResponse(job_id="JOB-LOCAL", report_id=report.report_id, status="complete", raw_count=len(raw_items), enriched_count=len(enriched), entity_count=len(names), panel_session_id=None)
