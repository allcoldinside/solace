import datetime as dt

import pytest

from cold_logic import (
    clean_mention,
    format_daily_mark,
    get_user_history,
    mark_for_date,
    normalize_anthropic_messages,
    save_to_memory,
    setup_database,
)


def test_memory_roundtrip_uses_chronological_order(tmp_path):
    db_path = tmp_path / "cold_logic.db"
    setup_database(str(db_path))

    save_to_memory(42, "Cold", "user", "first", db_path=str(db_path))
    save_to_memory(42, "Cold", "assistant", "second", db_path=str(db_path))
    save_to_memory(42, "Cold", "user", "third", db_path=str(db_path))

    assert get_user_history(42, str(db_path), limit=2) == [
        {"role": "assistant", "content": "second"},
        {"role": "user", "content": "third"},
    ]


def test_save_to_memory_rejects_invalid_roles(tmp_path):
    db_path = tmp_path / "cold_logic.db"
    setup_database(str(db_path))

    with pytest.raises(ValueError):
        save_to_memory(42, "Cold", "system", "no", db_path=str(db_path))


def test_daily_mark_rotation_and_format_are_stable():
    mark = mark_for_date(dt.date(2026, 6, 10))
    text = format_daily_mark(mark)

    assert mark["number"] == 2
    assert text.startswith("── MARK 02 · NETWORK ──")
    assert "Maxim:" in text
    assert "Counterfeit:" in text


def test_clean_mention_handles_nickname_mentions():
    assert clean_mention("<@!12345> what is the mark", 12345) == "what is the mark"
    assert clean_mention("<@12345> report", 12345) == "report"


def test_normalize_anthropic_messages_starts_with_user_and_merges_same_role_turns():
    history = [
        {"role": "assistant", "content": "orphan"},
        {"role": "user", "content": "one"},
        {"role": "user", "content": "two"},
        {"role": "assistant", "content": "three"},
    ]

    assert normalize_anthropic_messages(history) == [
        {"role": "user", "content": "one\n\ntwo"},
        {"role": "assistant", "content": "three"},
    ]
