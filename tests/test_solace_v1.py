"""SOLACE v1 smoke tests."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-for-jwt")
os.environ.setdefault("POSTGRES_URL", "postgresql+asyncpg://user:pass@localhost/test")


def test_app_imports():
    from api.main import app
    assert app.title == "SOLACE"


def test_password_hash_verify():
    from security.passwords import hash_password, verify_password
    hashed = hash_password("correct horse battery staple")
    assert hashed != "correct horse battery staple"
    assert verify_password("correct horse battery staple", hashed)
    assert not verify_password("wrong", hashed)


def test_auth_token_roundtrip():
    from security.auth import create_access_token, decode_token
    token, jti, _ = create_access_token("USER-1", "default", "admin")
    payload = decode_token(token)
    assert payload["sub"] == "USER-1"
    assert payload["tenant_id"] == "default"
    assert payload["role"] == "admin"
    assert payload["jti"] == jti


@pytest.mark.asyncio
async def test_seed_pipeline_runs_end_to_end():
    from core.schemas import PipelineRequest, TargetType
    from tasks.pipeline import run_pipeline
    response = await run_pipeline(None, PipelineRequest(target="Acme Corporation", target_type=TargetType.organization), None)
    assert response.status == "complete"
    assert response.report_id.startswith("REPORT-")
    assert response.raw_count >= 1


def test_report_invariants_validate():
    from core.invariants import validate_report
    from reports.generator import generate_report
    report = generate_report("Acme", "organization", [{"collector_id": "SEED", "source_url": "seed://x", "content_hash": "abc"}], {"candidates": ["Acme"]})
    validate_report(report)
    assert report.full_markdown


def test_queue_mapping():
    from tasks.priority import queue_for_priority
    assert queue_for_priority("critical") == "critical"
    assert queue_for_priority("nonsense") == "default"

@pytest.mark.asyncio
async def test_entity_resolver_extraction():
    from intelligence.entity_resolution import resolve_entities
    entities = await resolve_entities([{"content": "Acme Corporation operates in Central Florida."}])
    names = {item["name"] for item in entities}
    assert any("Acme" in name for name in names)
