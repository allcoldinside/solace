"""Panel domain models (non-ORM).  ORM model lives in core.models.PanelSessionRecord."""
from dataclasses import dataclass, field


@dataclass
class AnalystProfile:
    codename: str
    model: str
    role: str


DEFAULT_ANALYSTS: list[AnalystProfile] = [
    AnalystProfile("ALPHA", "stub", "OSINT methodology + behavioral analysis"),
    AnalystProfile("BRAVO", "stub", "Human patterns + influence mapping"),
    AnalystProfile("CHARLIE", "stub", "Technical infrastructure + vulnerability assessment"),
    AnalystProfile("DELTA", "stub", "Financial + supply chain analysis"),
    AnalystProfile("ECHO", "stub", "Synthesis + strategic assessment"),
]


@dataclass
class PanelResult:
    session_id: str
    report_id: str
    summary: str
    transcript: list[str] = field(default_factory=list)
    analyst_count: int = 2
