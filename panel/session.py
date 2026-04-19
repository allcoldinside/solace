"""Panel session state container."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from core.schemas import AnalystID, Disagreement, PanelStatus, PanelTurn
from reports.schema import generate_session_id


@dataclass
class PanelSessionState:
    """Tracks round-by-round panel state and transcript."""

    report_id: str
    topic: str
    target: str
    report_content: str
    session_id: str = field(default_factory=generate_session_id)
    history: list[PanelTurn] = field(default_factory=list)
    positions: dict[str, list[str]] = field(default_factory=dict)
    covered_topics: dict[str, int] = field(default_factory=dict)
    disagreements: list[Disagreement] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    round: int = 0
    max_rounds: int = 6
    concluded: bool = False
    status: PanelStatus = PanelStatus.ACTIVE
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime | None = None
    final_synthesis: str = ""

    def add_turn(self, analyst: AnalystID, content: str, is_loop_flagged: bool = False) -> PanelTurn:
        """Append turn to transcript."""
        turn = PanelTurn(
            analyst=analyst,
            content=content,
            round_number=self.round,
            is_loop_flagged=is_loop_flagged,
        )
        self.history.append(turn)
        return turn

    def record_position(self, analyst_id: str, content: str) -> None:
        """Store truncated position text by analyst."""
        stored = content[:300]
        self.positions.setdefault(analyst_id, []).append(stored)

    def add_disagreement(
        self,
        round_number: int,
        topic: str,
        alpha_position: str,
        bravo_position: str,
    ) -> None:
        """Record disagreement between Alpha and Bravo."""
        self.disagreements.append(
            Disagreement(
                round_number=round_number,
                topic=topic,
                alpha_position=alpha_position,
                bravo_position=bravo_position,
            )
        )

    def mark_covered(self, topic_key: str) -> None:
        """Mark topic as covered in current round."""
        normalized = topic_key.strip().lower()
        if normalized and normalized not in self.covered_topics:
            self.covered_topics[normalized] = self.round

    def get_recent_context(self, n_turns: int = 6) -> str:
        """Format recent transcript context for prompts."""
        recent_turns = self.history[-n_turns:]
        return "\n".join(f"[{turn.analyst.value}] {turn.content}" for turn in recent_turns)

    def get_formatted_transcript(self) -> str:
        """Render full transcript text."""
        return "\n".join(
            f"Round {turn.round_number} | {turn.analyst.value}: {turn.content}" for turn in self.history
        )

    @property
    def duration_str(self) -> str:
        """Compute human-readable session duration."""
        end = self.end_time or datetime.utcnow()
        total_seconds = max(0, int((end - self.start_time).total_seconds()))
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}m {seconds}s"

    def to_db_dict(self) -> dict[str, object]:
        """Serialize state for persistence."""
        return {
            "session_id": self.session_id,
            "report_id": self.report_id,
            "topic": self.topic,
            "target": self.target,
            "transcript": [turn.model_dump(mode="json") for turn in self.history],
            "positions": self.positions,
            "covered_topics": sorted(self.covered_topics.keys()),
            "disagreements": [item.model_dump(mode="json") for item in self.disagreements],
            "rounds_completed": self.round,
            "final_synthesis": self.final_synthesis,
            "concluded": self.concluded,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
