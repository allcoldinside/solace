"""Scheduled monitor helpers for enterprise workflows."""

from __future__ import annotations

from datetime import datetime, timedelta


def next_run(interval_hours: int) -> datetime:
    """Compute next scheduled run timestamp."""
    return datetime.now(timezone.utc) + timedelta(hours=interval_hours)
