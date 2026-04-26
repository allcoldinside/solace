"""Queue selection helpers."""

from __future__ import annotations

from tasks.queues import CRITICAL, DEFAULT, HIGH, LOW


def queue_for_priority(priority: str | None) -> str:
    value = (priority or DEFAULT).lower()
    if value in {LOW, DEFAULT, HIGH, CRITICAL}:
        return value
    return DEFAULT
