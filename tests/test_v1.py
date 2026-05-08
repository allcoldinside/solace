import asyncio
import os

os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./test_solace.db'
os.environ['SECRET_KEY'] = 'x' * 40

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from api.main import app
from core.models import Base
from core.schemas import (
    ClassificationLevel, ConfidenceLevel, CollectorID, TargetType,
    PanelStatus, AnalystID,
)
from security.passwords import hash_password, verify_password
from security.auth import create_access_token, decode_token
from tasks.priority import queue_for
from intelligence.entity_resolution import extract_candidates
from reports.schema import ReportData, new_report_id, generate_session_id
from core.invariants import validate_report


def setup_module():
    async def _init():
        engine = create_async_engine(os.environ['DATABASE_URL'])
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
    asyncio.run(_init())


client = TestClient(app)


# ── app ─────────────────────────────────────────────────────────────────────

def test_app_imports():
    assert app.title == 'SOLACE'


def test_health_endpoint():
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_system_info_endpoint():
    r = client.get('/api/system/info')
    assert r.status_code == 200
    assert 'name' in r.json()


def test_maintenance_endpoint():
    r = client.get('/api/maintenance')
    assert r.status_code == 200


# ── auth ─────────────────────────────────────────────────────────────────────

def test_password_roundtrip():
    h = hash_password('Secret123!')
    assert verify_password('Secret123!', h)
    assert not verify_password('wrong', h)


def test_token_roundtrip():
    t = create_access_token('user@example.com', 'default', 'admin')
    c = decode_token(t)
    assert c['tenant_id'] == 'default'
    assert c['role'] == 'admin'
    assert c['type'] == 'access'
    assert 'jti' in c


def test_register_and_login():
    client.post('/api/auth/register', json={
        'email': 'alice@test.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'default'
    })
    r = client.post('/api/auth/login', json={'email': 'alice@test.com', 'password': 'password123'})
    assert r.status_code == 200
    data = r.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_login_bad_credentials():
    r = client.post('/api/auth/login', json={'email': 'nobody@test.com', 'password': 'wrong'})
    assert r.status_code == 401


def test_me_endpoint():
    client.post('/api/auth/register', json={
        'email': 'bob@test.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'default'
    })
    r = client.post('/api/auth/login', json={'email': 'bob@test.com', 'password': 'password123'})
    token = r.json()['access_token']
    me = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert me.status_code == 200
    assert me.json()['email'] == 'bob@test.com'


def test_protected_route_unauthenticated():
    r = client.get('/api/reports')
    assert r.status_code in (401, 403)


def test_refresh_flow():
    client.post('/api/auth/register', json={
        'email': 'refresh@test.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'default'
    })
    r = client.post('/api/auth/login', json={'email': 'refresh@test.com', 'password': 'password123'})
    rt = r.json()['refresh_token']
    ref = client.post('/api/auth/refresh', json={'refresh_token': rt})
    assert ref.status_code == 200
    assert 'access_token' in ref.json()


# ── pipeline ─────────────────────────────────────────────────────────────────

def _admin_token() -> str:
    client.post('/api/auth/register', json={
        'email': 'admin@test.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'default'
    })
    r = client.post('/api/auth/login', json={'email': 'admin@test.com', 'password': 'password123'})
    return r.json()['access_token']


def test_pipeline_seed_e2e():
    token = _admin_token()
    r = client.post(
        '/api/pipeline/run',
        json={'target': 'Acme Corp', 'target_type': 'organization'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert r.status_code == 200
    data = r.json()
    assert data['report_id'].startswith('REPORT-')
    assert data['session_id'].startswith('SESSION-')
    assert isinstance(data['entities_saved'], int)


def test_reports_list():
    token = _admin_token()
    r = client.get('/api/reports', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_cases_crud():
    token = _admin_token()
    headers = {'Authorization': f'Bearer {token}'}
    cr = client.post('/api/cases', json={'title': 'Test Case', 'description': 'desc'}, headers=headers)
    assert cr.status_code == 200
    case_id = cr.json()['case_id']
    gr = client.get(f'/api/cases/{case_id}', headers=headers)
    assert gr.status_code == 200


def test_watches_crud():
    token = _admin_token()
    headers = {'Authorization': f'Bearer {token}'}
    wr = client.post('/api/watches', json={'target': 'test.com', 'target_type': 'infrastructure'}, headers=headers)
    assert wr.status_code == 200
    watch_id = wr.json()['watch_id']
    gr = client.get(f'/api/watches/{watch_id}', headers=headers)
    assert gr.status_code == 200


def test_entities_list():
    token = _admin_token()
    r = client.get('/api/entities', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_search_endpoint():
    token = _admin_token()
    r = client.get('/api/search?q=Acme', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200


def test_memory_endpoint():
    token = _admin_token()
    r = client.get('/api/memory', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200


def test_graph_endpoint():
    token = _admin_token()
    r = client.get('/api/graph', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200


# ── invariants & schemas ──────────────────────────────────────────────────────

def test_report_invariant():
    rd = ReportData('REPORT-X', 'a', 'organization', 'TLP:WHITE', 'MEDIUM', 0.5, 'sum', ['k'], full_markdown='ok')
    validate_report(rd)


def test_report_id_format():
    rid = new_report_id()
    assert rid.startswith('REPORT-')


def test_session_id_format():
    sid = generate_session_id()
    assert sid.startswith('SESSION-')


def test_queue_mapping():
    assert queue_for('critical') == 'critical'
    assert queue_for('high') == 'high'
    assert queue_for('low') == 'low'
    assert queue_for('unknown') == 'default'


def test_entity_extraction():
    cands = extract_candidates('Acme Corp works with Jane Doe')
    assert any(c['name'] == 'Acme' for c in cands)


def test_classification_level_enum():
    assert ClassificationLevel.tlp_white.value == 'TLP:WHITE'
    assert ClassificationLevel.tlp_red.value == 'TLP:RED'


def test_confidence_level_enum():
    assert ConfidenceLevel.high.value == 'HIGH'
    assert ConfidenceLevel.confirmed.value == 'CONFIRMED'


def test_collector_id_enum():
    assert CollectorID.SEED.value == 'SEED'
    assert CollectorID.SPIDER_23.value == 'SPIDER-23'


def test_panel_status_enum():
    assert PanelStatus.ACTIVE.value == 'ACTIVE'
    assert PanelStatus.CONCLUDED.value == 'CONCLUDED'


def test_analyst_id_enum():
    assert AnalystID.ALPHA.value == 'ANALYST-ALPHA'
    assert AnalystID.DIRECTOR.value == 'SESSION-DIRECTOR'


def test_target_type_enum():
    assert TargetType.organization.value == 'organization'
    assert TargetType.infrastructure.value == 'infrastructure'
