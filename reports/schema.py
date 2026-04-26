"""Canonical report dataclass and ID helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import re
import secrets


def _slugify(value: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    cleaned = re.sub(r"-{2,}", "-", compact)
    return cleaned.upper()[:40] or "UNKNOWN"


def generate_report_id(subject: str) -> str:
    return f"REPORT-{datetime.utcnow().strftime('%Y%m%d')}-{_slugify(subject)}-{secrets.token_hex(4).upper()}"


def generate_session_id() -> str:
    return f"SESSION-{secrets.token_hex(4).upper()}"


@dataclass
class ReportData:
    report_id: str
    subject: str
    subject_type: str
    classification: str = "TLP:WHITE"
    confidence: str = "MEDIUM"
    confidence_score: float = 0.5
    executive_summary: str = ""
    key_findings: list[str] = field(default_factory=list)
    entity_map: dict[str, Any] = field(default_factory=dict)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    behavioral_indicators: list[str] = field(default_factory=list)
    threat_assessment: dict[str, Any] = field(default_factory=dict)
    source_log: list[dict[str, Any]] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    analyst_notes: list[str] = field(default_factory=list)
    full_markdown: str = ""

    def to_markdown(self) -> str:
        def bullets(lines: list[Any]) -> str:
            return "\n".join(f"- {line}" for line in lines) if lines else "- None"
        timeline = "\n".join(f"- {item.get('date','unknown')}: {item.get('event','')}" for item in self.timeline) if self.timeline else "- None"
        sources = "\n".join(f"- {item.get('collector','unknown')}: {item.get('url','seed')}" for item in self.source_log) if self.source_log else "- None"
        text = (
            f"# {self.report_id}\n\n"
            f"Subject: {self.subject}\n\n"
            f"Classification: {self.classification}\n\n"
            "## EXECUTIVE SUMMARY\n" + self.executive_summary + "\n\n"
            "## KEY FINDINGS\n" + bullets(self.key_findings) + "\n\n"
            "## ENTITY MAP\n" + bullets([f"{k}: {v}" for k, v in self.entity_map.items()]) + "\n\n"
            "## TIMELINE\n" + timeline + "\n\n"
            "## BEHAVIORAL INDICATORS\n" + bullets(self.behavioral_indicators) + "\n\n"
            "## THREAT ASSESSMENT\n" + str(self.threat_assessment) + "\n\n"
            "## SOURCE LOG\n" + sources + "\n\n"
            "## GAPS & COLLECTION REQUIREMENTS\n" + bullets(self.gaps) + "\n\n"
            "## ANALYST NOTES\n" + bullets(self.analyst_notes) + "\n"
        )
        self.full_markdown = text
        return text
