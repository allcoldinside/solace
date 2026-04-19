"""SOLACE Enterprise five-analyst orchestration engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalystProfile:
    """Analyst model profile.

    Attributes:
        codename: Analyst codename.
        model: Model identifier.
        role: Specialized role description.
    """

    codename: str
    model: str
    role: str


class EnterprisePanelEngine:
    """Coordinates enterprise five-analyst mode session composition."""

    def __init__(self) -> None:
        """Initialize analyst lineup."""
        self.analysts = [
            AnalystProfile("ANALYST-ALPHA", "claude-opus", "OSINT methodology + behavioral analysis"),
            AnalystProfile("ANALYST-BRAVO", "gpt-4o", "Human patterns + influence mapping"),
            AnalystProfile("SESSION-DIRECTOR", "gemini-1.5-pro", "Panel management + synthesis"),
            AnalystProfile("ANALYST-GAMMA", "claude-haiku", "Geopolitical and regional context specialist"),
            AnalystProfile("ANALYST-DELTA", "gpt-4o-mini", "Technical infrastructure and capability specialist"),
        ]

    def get_session_blueprint(self) -> dict[str, list[dict[str, str]]]:
        """Return serializable session blueprint for UI or API use."""
        return {
            "analysts": [
                {"codename": analyst.codename, "model": analyst.model, "role": analyst.role}
                for analyst in self.analysts
            ]
        }
