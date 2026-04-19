"""Report schema utilities for SOLACE."""

from dataclasses import dataclass, field
from datetime import datetime
import re
import secrets


def _slugify(value: str) -> str:
    """Create a safe uppercase slug.

    Args:
        value: Arbitrary source string.

    Returns:
        Hyphenated uppercase token.
    """
    compact = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    cleaned = re.sub(r"-{2,}", "-", compact)
    return cleaned.upper() or "UNKNOWN"


def generate_report_id(subject: str) -> str:
    """Generate deterministic-format report identifier.

    Args:
        subject: Report target subject.

    Returns:
        Identifier formatted as REPORT-YYYYMMDD-SLUG-RANDOM.
    """
    date_part = datetime.utcnow().strftime("%Y%m%d")
    slug = _slugify(subject)
    suffix = secrets.token_hex(4).upper()
    return f"REPORT-{date_part}-{slug}-{suffix}"


def generate_session_id() -> str:
    """Generate panel session identifier."""
    return f"SESSION-{secrets.token_hex(4).upper()}"


@dataclass
class ReportData:
    """Structured report data container."""

    report_id: str
    subject: str
    executive_summary: str
    key_findings: list[str]
    entity_map: dict[str, list[str]] = field(default_factory=dict)
    timeline: list[str] = field(default_factory=list)
    behavioral_indicators: list[str] = field(default_factory=list)
    source_log: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    analyst_notes: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Render report using required section headers.

        Returns:
            Markdown report text.
        """
        findings = "\n".join(f"- {line}" for line in self.key_findings) or "- None"
        timeline = "\n".join(f"- {line}" for line in self.timeline) or "- None"
        behaviors = "\n".join(f"- {line}" for line in self.behavioral_indicators) or "- None"
        sources = "\n".join(f"- {line}" for line in self.source_log) or "- None"
        gaps = "\n".join(f"- {line}" for line in self.gaps) or "- None"
        notes = "\n".join(f"- {line}" for line in self.analyst_notes) or "- None"
        entity_lines = []
        for category, values in self.entity_map.items():
            entity_lines.append(f"- **{category}**: {', '.join(values) if values else 'None'}")
        entity_map = "\n".join(entity_lines) or "- None"
        return (
            f"# {self.report_id}\n\n"
            "## EXECUTIVE SUMMARY\n"
            f"{self.executive_summary}\n\n"
            "## KEY FINDINGS\n"
            f"{findings}\n\n"
            "## ENTITY MAP\n"
            f"{entity_map}\n\n"
            "## TIMELINE\n"
            f"{timeline}\n\n"
            "## BEHAVIORAL INDICATORS\n"
            f"{behaviors}\n\n"
            "## SOURCE LOG\n"
            f"{sources}\n\n"
            "## GAPS & COLLECTION REQUIREMENTS\n"
            f"{gaps}\n\n"
            "## ANALYST NOTES\n"
            f"{notes}\n"
        )
