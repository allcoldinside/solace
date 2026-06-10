import asyncio
import os

os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test_solace.db')
os.environ.setdefault('SECRET_KEY', 'x' * 40)

from fastapi.testclient import TestClient

from api.main import app
from processing.pipeline import chunk_text, clean_html, normalize_whitespace
from tasks.document_processing import process_document
from intelligence.entity_extractor import extract_entities

from sqlalchemy.ext.asyncio import create_async_engine
from core.models import Base


def setup_module():
    async def _init():
        engine = create_async_engine(os.environ['DATABASE_URL'])
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
    asyncio.run(_init())


def test_chunk_text_offsets():
    text = 'a' * 1200
    chunks = chunk_text(text, chunk_size=500)
    assert len(chunks) == 3
    assert chunks[0]['start_offset'] == 0
    assert chunks[0]['end_offset'] == 500
    assert chunks[2]['start_offset'] == 1000


def test_normalization_and_html_cleaning():
    assert normalize_whitespace('a\n\n b\t c') == 'a b c'
    assert clean_html('<p>Hello</p>  <b>World</b>') == 'Hello World'


def test_process_document_task_logic():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'proc@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'proc-tenant'})
    login = client.post('/api/auth/login', json={'email': 'proc@a.com', 'password': 'password123'})
    token = login.json()['access_token']
    case = client.post('/api/cases', json={'title': 'Proc Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']

    up = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('doc.txt', b'hello world ' * 100, 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    assert up.status_code == 200
    document_id = up.json()['document_id']

    result = asyncio.run(process_document(document_id))
    assert result['document_id'] == document_id
    assert result['chunks'] >= 1


def test_entity_extraction_basics():
    text = 'Alice Smith works at Acme Corp and email alice@example.com'
    entities = extract_entities(text)
    names = {e['canonical_name'] for e in entities}
    assert 'alice@example.com' in names
    assert 'Alice Smith' in names
