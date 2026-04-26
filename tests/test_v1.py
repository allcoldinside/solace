import asyncio
import os
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./test_solace.db'
os.environ['SECRET_KEY'] = 'x' * 40

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from api.main import app
from core.models import Base
from security.passwords import hash_password, verify_password
from security.auth import create_access_token, decode_token
from tasks.priority import queue_for
from intelligence.entity_resolution import extract_candidates
from reports.schema import ReportData
from core.invariants import validate_report


def setup_module():
    async def _init():
        engine = create_async_engine(os.environ['DATABASE_URL'])
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
    asyncio.run(_init())


def test_app_imports():
    assert app.title == 'SOLACE'


def test_password_roundtrip():
    h = hash_password('Secret123!')
    assert verify_password('Secret123!', h)


def test_token_roundtrip():
    t = create_access_token('user@example.com', 'default', 'admin')
    c = decode_token(t)
    assert c['tenant_id'] == 'default'


def test_pipeline_seed_e2e():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email':'a@a.com','password':'password123','role':'admin','tenant_id':'default'})
    l = client.post('/api/auth/login', json={'email':'a@a.com','password':'password123'})
    token = l.json()['access_token']
    r = client.post('/api/pipeline/run', json={'target':'Acme Corp','target_type':'organization'}, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    assert r.json()['report_id'].startswith('REPORT-')


def test_report_invariant():
    rd = ReportData('REPORT-X','a','organization','TLP:WHITE','MEDIUM',0.5,'sum',['k'],full_markdown='ok')
    validate_report(rd)


def test_queue_mapping():
    assert queue_for('critical') == 'critical'
    assert queue_for('unknown') == 'default'


def test_entity_extraction():
    cands = extract_candidates('Acme Corp works with Jane Doe')
    assert any(c['name'] == 'Acme' for c in cands)
