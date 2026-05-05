"""Comprehensive v2 tests: auth flows, tenant isolation, validation, schemas, entity dedup, audit log."""
import asyncio
import os
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test_solace.db')
os.environ.setdefault('SECRET_KEY', 'y' * 40)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.main import app
from core.models import Base, AuditLog
from core.schemas import (
    CollectorID, RawIntelItemSchema, CollectionResult,
    PipelineRequest, TargetType, LoginRequest, RegisterRequest,
)
from security.auth import create_access_token, create_refresh_token, decode_token
from storage.entity_store import EntityStore
from storage.audit_store import AuditStore

_DB_URL = os.environ['DATABASE_URL']


def setup_module():
    async def _init():
        engine = create_async_engine(_DB_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
    asyncio.run(_init())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

client = TestClient(app)


def _register(email: str, password: str = 'password123', role: str = 'analyst', tenant: str = 'default') -> dict:
    r = client.post('/api/auth/register', json={
        'email': email, 'password': password, 'role': role, 'tenant_id': tenant,
    })
    return r


def _login(email: str, password: str = 'password123') -> dict:
    r = client.post('/api/auth/login', json={'email': email, 'password': password})
    return r.json()


def _auth(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}


# ---------------------------------------------------------------------------
# Schema round-trips
# ---------------------------------------------------------------------------

def test_collector_id_enum_known():
    assert CollectorID('SPIDER-9') == CollectorID.SPIDER_9


def test_collector_id_enum_unknown_passthrough():
    c = CollectorID('SPIDER-99')
    assert c.value == 'SPIDER-99'


def test_raw_intel_item_roundtrip():
    from datetime import datetime, timezone
    item = RawIntelItemSchema(
        content_hash='abc123',
        collector_id=CollectorID.SPIDER_9,
        source_url='https://example.com',
        source_type='web',
        content='some intel',
        target='Acme Corp',
        target_type=TargetType.organization,
        collected_at=datetime.now(timezone.utc),
    )
    d = item.model_dump()
    item2 = RawIntelItemSchema(**d)
    assert item2.content_hash == 'abc123'
    assert item2.collector_id == CollectorID.SPIDER_9


def test_collection_result_empty():
    cr = CollectionResult(collector_id=CollectorID.SEED)
    assert cr.items == []


def test_pipeline_request_strips_whitespace():
    req = PipelineRequest(target='  Acme Corp  ', target_type=TargetType.organization)
    assert req.target == 'Acme Corp'


def test_pipeline_request_rejects_blank():
    with pytest.raises(Exception):
        PipelineRequest(target='   ')


def test_pipeline_request_too_long():
    with pytest.raises(Exception):
        PipelineRequest(target='x' * 513)


def test_login_request_rejects_bad_email():
    with pytest.raises(Exception):
        LoginRequest(email='not-an-email', password='password123')


def test_register_request_rejects_short_password():
    with pytest.raises(Exception):
        RegisterRequest(email='u@u.com', password='short')


# ---------------------------------------------------------------------------
# Auth flows
# ---------------------------------------------------------------------------

def test_register_and_login():
    r = _register('v2_user@example.com', role='admin')
    assert r.status_code == 200

    tokens = _login('v2_user@example.com')
    assert 'access_token' in tokens
    assert 'refresh_token' in tokens


def test_login_bad_credentials():
    _register('v2_bad@example.com')
    r = client.post('/api/auth/login', json={'email': 'v2_bad@example.com', 'password': 'wrong'})
    assert r.status_code == 401


def test_duplicate_email_rejected():
    _register('v2_dup@example.com')
    r2 = _register('v2_dup@example.com')
    assert r2.status_code == 400


def test_me_endpoint():
    _register('v2_me@example.com', role='admin')
    tokens = _login('v2_me@example.com')
    r = client.get('/api/auth/me', headers=_auth(tokens['access_token']))
    assert r.status_code == 200
    data = r.json()
    assert data['email'] == 'v2_me@example.com'
    assert data['role'] == 'admin'


def test_logout_revokes_access_token():
    _register('v2_logout@example.com', role='admin')
    tokens = _login('v2_logout@example.com')
    access = tokens['access_token']
    refresh = tokens['refresh_token']

    r = client.post('/api/auth/logout',
                    json={'refresh_token': refresh},
                    headers=_auth(access))
    assert r.status_code == 200

    # Access token is now revoked — any protected endpoint should 401
    r2 = client.get('/api/auth/me', headers=_auth(access))
    assert r2.status_code == 401


def test_refresh_issues_new_tokens():
    _register('v2_refresh@example.com', role='admin')
    tokens = _login('v2_refresh@example.com')
    r = client.post('/api/auth/refresh', json={'refresh_token': tokens['refresh_token']})
    assert r.status_code == 200
    new_tokens = r.json()
    assert 'access_token' in new_tokens
    assert new_tokens['access_token'] != tokens['access_token']


def test_refresh_with_access_token_rejected():
    _register('v2_wrongtype@example.com', role='admin')
    tokens = _login('v2_wrongtype@example.com')
    r = client.post('/api/auth/refresh', json={'refresh_token': tokens['access_token']})
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Tenant isolation
# ---------------------------------------------------------------------------

def test_cross_tenant_isolation():
    _register('tenant_a@example.com', tenant='tenant-a')
    _register('tenant_b@example.com', tenant='tenant-b')

    a_tokens = _login('tenant_a@example.com')
    b_tokens = _login('tenant_b@example.com')

    # tenant-a creates a case
    r = client.post('/api/cases', json={'title': 'Tenant A case'},
                    headers=_auth(a_tokens['access_token']))
    assert r.status_code == 200
    case_id = r.json()['case_id']

    # tenant-b cannot see tenant-a's case
    r2 = client.get(f'/api/cases/{case_id}', headers=_auth(b_tokens['access_token']))
    assert r2.status_code == 404


# ---------------------------------------------------------------------------
# 404 paths
# ---------------------------------------------------------------------------

def test_case_404():
    _register('v2_cases@example.com', role='admin')
    tokens = _login('v2_cases@example.com')
    r = client.get('/api/cases/NONEXISTENT-CASE', headers=_auth(tokens['access_token']))
    assert r.status_code == 404


def test_watch_404():
    _register('v2_watches@example.com', role='admin')
    tokens = _login('v2_watches@example.com')
    r = client.get('/api/watches/NONEXISTENT-WATCH', headers=_auth(tokens['access_token']))
    assert r.status_code == 404


def test_panel_404():
    _register('v2_panel@example.com', role='admin')
    tokens = _login('v2_panel@example.com')
    r = client.get('/api/panel/NONEXISTENT-SESSION', headers=_auth(tokens['access_token']))
    assert r.status_code == 404


def test_report_404():
    _register('v2_report@example.com', role='admin')
    tokens = _login('v2_report@example.com')
    r = client.get('/api/reports/NONEXISTENT-REPORT', headers=_auth(tokens['access_token']))
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

def test_audit_log_written_on_register_and_login():
    engine = create_async_engine(_DB_URL)

    async def _check():
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with Session() as db:
            store = AuditStore(db)
            logs = await store.list('default')
            actions = [l.action for l in logs]
        await engine.dispose()
        return actions

    _register('v2_audit@example.com', role='admin', tenant='default')
    _login('v2_audit@example.com')

    actions = asyncio.run(_check())
    assert 'register' in actions
    assert 'login' in actions


# ---------------------------------------------------------------------------
# Entity deduplication
# ---------------------------------------------------------------------------

def test_entity_upsert_deduplication():
    engine = create_async_engine(_DB_URL)

    async def _run():
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with Session() as db:
            store = EntityStore(db)
            e1 = await store.upsert('dedup-tenant', 'Acme Corp', 'organization', confidence=0.6)
            e2 = await store.upsert('dedup-tenant', 'Acme Corp', 'organization', confidence=0.9)
            entities = await store.list('dedup-tenant')
        await engine.dispose()
        return e1.entity_id, e2.entity_id, entities

    e1_id, e2_id, entities = asyncio.run(_run())
    assert e1_id == e2_id
    acme = [e for e in entities if e.name == 'Acme Corp']
    assert len(acme) == 1
    assert acme[0].confidence == 0.9


def test_entity_different_kind_not_deduplicated():
    engine = create_async_engine(_DB_URL)

    async def _run():
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with Session() as db:
            store = EntityStore(db)
            e1 = await store.upsert('kind-tenant', 'AcmeX', 'organization', confidence=0.5)
            e2 = await store.upsert('kind-tenant', 'AcmeX', 'person', confidence=0.5)
            entities = await store.list('kind-tenant')
        await engine.dispose()
        return e1.entity_id, e2.entity_id, entities

    e1_id, e2_id, entities = asyncio.run(_run())
    assert e1_id != e2_id
    acmex = [e for e in entities if e.name == 'AcmeX']
    assert len(acmex) == 2


# ---------------------------------------------------------------------------
# Search returns empty list when nothing matches
# ---------------------------------------------------------------------------

def test_search_empty_results():
    _register('v2_search@example.com', role='admin')
    tokens = _login('v2_search@example.com')
    r = client.get('/api/search?q=zzznoresultsxxx', headers=_auth(tokens['access_token']))
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 0


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_health_endpoint():
    r = client.get('/api/health')
    assert r.status_code == 200
    data = r.json()
    assert data.get('status') == 'ok'


# ---------------------------------------------------------------------------
# Token decode properties
# ---------------------------------------------------------------------------

def test_access_token_claims():
    token = create_access_token('u@u.com', 'my-tenant', 'admin')
    claims = decode_token(token)
    assert claims['sub'] == 'u@u.com'
    assert claims['tenant_id'] == 'my-tenant'
    assert claims['role'] == 'admin'
    assert claims['type'] == 'access'


def test_refresh_token_claims():
    token = create_refresh_token('u@u.com', 'my-tenant', 'analyst')
    claims = decode_token(token)
    assert claims['type'] == 'refresh'


def test_tampered_token_rejected():
    token = create_access_token('u@u.com', 'default', 'admin')
    parts = token.split('.')
    tampered = parts[0] + '.' + parts[1] + '.badsignature'
    with pytest.raises(ValueError):
        decode_token(tampered)
