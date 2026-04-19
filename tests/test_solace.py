"""Core tests for SOLACE scaffold components."""

from __future__ import annotations

import os

os.environ.setdefault("SECRET_KEY", "x" * 32)

from collectors.aggregator import AggregatorBot, SOURCE_RELIABILITY
from config.settings import Settings
from core.schemas import AnalystID, CollectionResult, CollectorID, PanelStatus, RawIntelItemSchema, TargetType
from panel.loop_detector import LoopDetector
from panel.prompts import CHATGPT_SYSTEM, CLAUDE_SYSTEM, GEMINI_SYSTEM, SYNTHESIS_PROMPT_TEMPLATE
from panel.session import PanelSessionState
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


class TestSettings:
    """Settings tests."""

    def test_settings_defaults(self) -> None:
        settings = Settings()
        assert settings.app_name == "SOLACE"
        assert settings.celery_broker_url == settings.redis_url
        assert settings.celery_result_backend == settings.redis_url


class TestReportSchema:
    """Report schema tests."""

    def test_report_identifiers_format(self) -> None:
        report_id = generate_report_id("Acme Corp")
        session_id = generate_session_id()
        assert report_id.startswith("REPORT-")
        assert "-ACME-CORP-" in report_id
        assert session_id.startswith("SESSION-")
        assert len(session_id) == 16

    def test_report_markdown_sections_present(self) -> None:
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


class TestAggregator:
    """Aggregator tests."""

    def test_aggregator_deduplicates_and_sorts(self) -> None:
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

    def test_source_reliability_count(self) -> None:
        assert len(SOURCE_RELIABILITY) == 19

    def test_aggregator_filters_short_items(self) -> None:
        bot = AggregatorBot()
        short_item = make_raw_item(content="short text")
        result = CollectionResult(collector_id=CollectorID.SPIDER_1, items=[short_item])
        output = bot.process([result])
        assert output == []


class TestPrompts:
    """Prompt completeness tests."""

    def test_prompt_lengths(self) -> None:
        assert len(CLAUDE_SYSTEM) > 500
        assert len(CHATGPT_SYSTEM) > 500
        assert len(GEMINI_SYSTEM) > 500

    def test_prompt_template_vars(self) -> None:
        for variable in ["{session_id}", "{report_id}", "{target}", "{transcript}"]:
            assert variable in SYNTHESIS_PROMPT_TEMPLATE


class TestLoopDetector:
    """Loop detector tests."""

    def test_empty_prior_never_loops(self) -> None:
        detector = LoopDetector(threshold=0.65)
        is_loop, matched, score = detector.is_loop("ANALYST-ALPHA", "new thought", [])
        assert is_loop is False
        assert matched is None
        assert score == 0.0

    def test_keyword_fallback_detects_identical_content(self) -> None:
        detector = LoopDetector(threshold=0.65)
        content = "financial offshore connections entity subject analysis"
        is_loop, _, score = detector._keyword_fallback(content, [content])
        assert is_loop is True
        assert score == 1.0

    def test_least_covered_section_prefers_uncovered_present_text(self) -> None:
        detector = LoopDetector()
        content = "This report includes behavioral indicators and timeline events only."
        section = detector.find_least_covered_section(content, ["timeline events"])
        assert section == "behavioral indicators"


class TestPanelSessionState:
    """Panel session state tests."""

    def test_add_turn_and_position(self) -> None:
        session = PanelSessionState(
            report_id="R1",
            topic="topic",
            target="target",
            report_content="content",
        )
        session.round = 1
        turn = session.add_turn(AnalystID.CLAUDE, "Alpha observation")
        session.record_position(AnalystID.CLAUDE.value, turn.content)
        assert len(session.history) == 1
        assert session.positions[AnalystID.CLAUDE.value][0] == "Alpha observation"

    def test_mark_covered_and_disagreement(self) -> None:
        session = PanelSessionState(
            report_id="R1",
            topic="topic",
            target="target",
            report_content="content",
            status=PanelStatus.ACTIVE,
        )
        session.round = 2
        session.mark_covered("Threat Assessment")
        session.add_disagreement(2, "threat", "alpha", "bravo")
        assert session.covered_topics["threat assessment"] == 2
        assert len(session.disagreements) == 1

    def test_serialization_contains_expected_fields(self) -> None:
        session = PanelSessionState(report_id="R1", topic="topic", target="target", report_content="content")
        session.final_synthesis = "final"
        payload = session.to_db_dict()
        assert payload["session_id"].startswith("SESSION-")
        assert payload["final_synthesis"] == "final"
        assert payload["concluded"] is False
