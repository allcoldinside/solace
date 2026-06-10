import os

os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test_solace.db')
os.environ.setdefault('SECRET_KEY', 'x' * 40)

from fastapi.testclient import TestClient

from api.main import app


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_dashboard_page_loads() -> None:
    client = TestClient(app)
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    assert 'SOLACE Dashboard MVP' in response.text
