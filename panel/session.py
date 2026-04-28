from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PanelStatus(str, Enum):
    ACTIVE = "active"
    CONCLUDED = "concluded"
    FAILED = "failed"


class AnalystID(str, Enum):
    ALPHA = "alpha"
    BRAVO = "bravo"
    CHARLIE = "charlie"
    DELTA = "delta"
    ECHO = "echo"


@dataclass
class PanelTurn:
    analyst: AnalystID
    content: str
    round_number: int = 0
    is_loop_flagged: bool = False

    def model_dump(self, **_) -> dict:
        return {
            "analyst": self.analyst.value,
            "content": self.content,
            "round_number": self.round_number,
            "is_loop_flagged": self.is_loop_flagged,
        }


@dataclass
class Disagreement:
    round_number: int
    topic: str
    alpha_position: str
    bravo_position: str

    def model_dump(self, **_) -> dict:
        return {
            "round_number": self.round_number,
            "topic": self.topic,
            "alpha_position": self.alpha_position,
            "bravo_position": self.bravo_position,
        }


def generate_session_id() -> str:
    return f"SESSION-{uuid.uuid4().hex[:10].upper()}"


@dataclass
class PanelSessionState:
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
        turn = PanelTurn(analyst=analyst, content=content, round_number=self.round, is_loop_flagged=is_loop_flagged)
        self.history.append(turn)
        return turn

    def record_position(self, analyst_id: str, content: str) -> None:
        self.positions.setdefault(analyst_id, []).append(content[:300])

    def add_disagreement(self, round_number: int, topic: str, alpha_position: str, bravo_position: str) -> None:
        self.disagreements.append(Disagreement(round_number=round_number, topic=topic, alpha_position=alpha_position, bravo_position=bravo_position))

    def mark_covered(self, topic_key: str) -> None:
        normalized = topic_key.strip().lower()
        if normalized and normalized not in self.covered_topics:
            self.covered_topics[normalized] = self.round

    def get_recent_context(self, n_turns: int = 6) -> str:
        return "\n".join(f"[{t.analyst.value}] {t.content}" for t in self.history[-n_turns:])

    def get_formatted_transcript(self) -> str:
        return "\n".join(f"Round {t.round_number} | {t.analyst.value}: {t.content}" for t in self.history)

    @property
    def duration_str(self) -> str:
        end = self.end_time or datetime.utcnow()
        total = max(0, int((end - self.start_time).total_seconds()))
        m, s = divmod(total, 60)
        return f"{m}m {s}s"

    def to_db_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "report_id": self.report_id,
            "topic": self.topic,
            "target": self.target,
            "transcript": [t.model_dump() for t in self.history],
            "positions": self.positions,
            "covered_topics": sorted(self.covered_topics.keys()),
            "disagreements": [d.model_dump() for d in self.disagreements],
            "rounds_completed": self.round,
            "final_synthesis": self.final_synthesis,
            "concluded": self.concluded,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
