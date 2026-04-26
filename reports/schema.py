from dataclasses import dataclass, field
import uuid


@dataclass
class ReportData:
    report_id: str
    subject: str
    subject_type: str
    classification: str
    confidence: str
    confidence_score: float
    executive_summary: str
    key_findings: list[str]
    entity_map: list[dict] = field(default_factory=list)
    timeline: list[str] = field(default_factory=list)
    behavioral_indicators: list[str] = field(default_factory=list)
    threat_assessment: str = ''
    source_log: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    analyst_notes: str = ''
    full_markdown: str = ''


def new_report_id() -> str:
    return f'REPORT-{uuid.uuid4().hex[:12].upper()}'
