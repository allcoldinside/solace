"""Core smoke tests for SOLACE scaffolding."""

import os

os.environ.setdefault("SECRET_KEY", "x" * 32)

from collectors.aggregator import AggregatorBot, SOURCE_RELIABILITY
from config.settings import Settings
from core.schemas import CollectionResult, CollectorID, RawIntelItemSchema, TargetType
from reports.schema import ReportData, generate_report_id, generate_session_id


def make_raw_item(**overrides: object) -> RawIntelItemSchema:
    """Create a minimal raw intel item for tests."""
    base = {
        "content_hash": "hash-1",
        "collector_id": CollectorID.SPIDER_1,
        "source_url": "https://example.com/a",
        "source_type": "news_rss",
        "content": "A" * 100,
        "target": "Acme Corp",
        "target_type": TargetType.ORGANIZATION,
        "reliability_score": 0.11,
    }
    base.update(overrides)
    return RawIntelItemSchema(**base)


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.app_name == "SOLACE"
    assert settings.celery_broker_url == settings.redis_url
    assert settings.celery_result_backend == settings.redis_url


def test_report_identifiers_format() -> None:
    report_id = generate_report_id("Acme Corp")
    session_id = generate_session_id()
    assert report_id.startswith("REPORT-")
    assert "-ACME-CORP-" in report_id
    assert session_id.startswith("SESSION-")
    assert len(session_id) == 16


def test_report_markdown_sections_present() -> None:
    report = ReportData(
        report_id="REPORT-20260101-ACME-CORP-ABCDEF12",
        subject="Acme Corp",
        executive_summary="Summary",
        key_findings=["Finding A"],
    )
    markdown = report.to_markdown()
    for heading in [
        "EXECUTIVE SUMMARY",
        "KEY FINDINGS",
        "ENTITY MAP",
        "TIMELINE",
        "BEHAVIORAL INDICATORS",
        "SOURCE LOG",
        "GAPS & COLLECTION REQUIREMENTS",
        "ANALYST NOTES",
    ]:
        assert f"## {heading}" in markdown


def test_aggregator_deduplicates_and_sorts() -> None:
    bot = AggregatorBot()
    a = make_raw_item(content_hash="same", source_type="reddit_post", content="B" * 100)
    b = make_raw_item(content_hash="same", source_type="cisa_advisory", content="B" * 100)
    c = make_raw_item(content_hash="unique", source_type="twitter_nitter", content="C" * 100)
    results = [
        CollectionResult(collector_id=CollectorID.SPIDER_1, items=[a, c]),
        CollectionResult(collector_id=CollectorID.SPIDER_2, items=[b]),
    ]
    output = bot.process(results)
    assert len(output) == 2
    assert output[0].reliability_score >= output[1].reliability_score


def test_source_reliability_count() -> None:
    assert len(SOURCE_RELIABILITY) == 19
