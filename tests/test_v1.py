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


def test_auth_audit_log_entries():
    client = TestClient(app)
    email = 'audit-user@a.com'
    password = 'password123'
    client.post('/api/auth/register', json={'email':email,'password':password,'role':'admin','tenant_id':'default'})
    login = client.post('/api/auth/login', json={'email':email,'password':password})
    token = login.json()['access_token']
    refresh_token = login.json()['refresh_token']

    audit_before = client.get('/api/audit', headers={'Authorization': f'Bearer {token}'})
    count_before = len(audit_before.json())

    logout = client.post('/api/auth/logout', json={'refresh_token': refresh_token})
    assert logout.status_code == 200

    audit_after = client.get('/api/audit', headers={'Authorization': f'Bearer {token}'})
    assert audit_after.status_code == 200
    actions = [item['action'] for item in audit_after.json()]
    assert 'auth.register' in actions
    assert 'auth.login' in actions
    assert 'auth.logout' in actions
    assert len(audit_after.json()) >= count_before


def test_login_failure_returns_401():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'badlogin@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-a'})
    response = client.post('/api/auth/login', json={'email': 'badlogin@a.com', 'password': 'wrong'})
    assert response.status_code == 401


def test_protected_endpoint_requires_authentication():
    client = TestClient(app)
    response = client.get('/api/system/protected')
    assert response.status_code == 401


def test_tenant_scoped_endpoint_rejects_outside_tenant():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'tenant-user@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-a'})
    login = client.post('/api/auth/login', json={'email': 'tenant-user@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    denied = client.get('/api/system/tenant-access', headers={'Authorization': f'Bearer {token}', 'X-Tenant-ID': 'tenant-b'})
    assert denied.status_code == 403

    allowed = client.get('/api/system/tenant-access', headers={'Authorization': f'Bearer {token}', 'X-Tenant-ID': 'tenant-a'})
    assert allowed.status_code == 200


def test_case_creation_writes_audit_record():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'caseaudit@a.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'default'})
    login = client.post('/api/auth/login', json={'email': 'caseaudit@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    created = client.post('/api/cases', json={'title': 'Case A', 'description': 'Desc'}, headers={'Authorization': f'Bearer {token}', 'X-Request-ID': 'req-1'})
    assert created.status_code == 200

    audit = client.get('/api/audit?action=case.create', headers={'Authorization': f'Bearer {token}'})
    assert audit.status_code == 200
    assert any(item['action'] == 'case.create' and item['request_id'] == 'req-1' for item in audit.json())


def test_pipeline_report_generation_writes_audit_record():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'reportaudit@a.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'default'})
    login = client.post('/api/auth/login', json={'email': 'reportaudit@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    run = client.post('/api/pipeline/run', json={'target': 'Acme Corp', 'target_type': 'organization'}, headers={'Authorization': f'Bearer {token}', 'X-Request-ID': 'req-2'})
    assert run.status_code == 200

    audit = client.get('/api/audit?action=report.generate', headers={'Authorization': f'Bearer {token}'})
    assert audit.status_code == 200
    assert any(item['action'] == 'report.generate' and item['request_id'] == 'req-2' for item in audit.json())


def test_case_crud_and_lifecycle_audit():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'caseflow@a.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'tenant-case'})
    login = client.post('/api/auth/login', json={'email': 'caseflow@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    created = client.post('/api/cases', json={'title': 'Lifecycle Case', 'description': 'd', 'priority': 'high'}, headers={'Authorization': f'Bearer {token}'})
    assert created.status_code == 200
    case_id = created.json()['case_id']

    patched = client.patch(f'/api/cases/{case_id}', json={'status': 'active'}, headers={'Authorization': f'Bearer {token}'})
    assert patched.status_code == 200
    assert patched.json()['status'] == 'active'

    archived = client.patch(f'/api/cases/{case_id}', json={'status': 'archived'}, headers={'Authorization': f'Bearer {token}'})
    assert archived.status_code == 200

    deleted = client.delete(f'/api/cases/{case_id}', headers={'Authorization': f'Bearer {token}'})
    assert deleted.status_code == 200

    audit = client.get('/api/audit?resource_type=case', headers={'Authorization': f'Bearer {token}'})
    actions = [item['action'] for item in audit.json()]
    assert 'case.create' in actions
    assert 'case.update' in actions
    assert 'case.archive' in actions
    assert 'case.delete' in actions


def test_user_cannot_access_other_tenant_case():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'tenant1@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-1'})
    login1 = client.post('/api/auth/login', json={'email': 'tenant1@a.com', 'password': 'password123'})
    token1 = login1.json()['access_token']
    case = client.post('/api/cases', json={'title': 'T1 Case', 'description': 'x'}, headers={'Authorization': f'Bearer {token1}'})
    case_id = case.json()['case_id']

    client.post('/api/auth/register', json={'email': 'tenant2@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-2'})
    login2 = client.post('/api/auth/login', json={'email': 'tenant2@a.com', 'password': 'password123'})
    token2 = login2.json()['access_token']

    denied = client.get(f'/api/cases/{case_id}', headers={'Authorization': f'Bearer {token2}'})
    assert denied.status_code == 404


def test_document_upload_stores_metadata_and_detects_duplicates():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'upload@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-upload'})
    login = client.post('/api/auth/login', json={'email': 'upload@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    created_case = client.post('/api/cases', json={'title': 'Upload Case', 'description': 'x'}, headers={'Authorization': f'Bearer {token}'})
    case_id = created_case.json()['case_id']

    files = {'file': ('note.txt', b'hello solace', 'text/plain')}
    uploaded = client.post(f'/api/cases/{case_id}/sources/upload', files=files, headers={'Authorization': f'Bearer {token}'})
    assert uploaded.status_code == 200
    assert uploaded.json()['sha256_hash']

    duplicate = client.post(f'/api/cases/{case_id}/sources/upload', files=files, headers={'Authorization': f'Bearer {token}'})
    assert duplicate.status_code == 409


def test_document_upload_respects_tenant_case_isolation():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'owner@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'owner-tenant'})
    owner_login = client.post('/api/auth/login', json={'email': 'owner@a.com', 'password': 'password123'})
    owner_token = owner_login.json()['access_token']
    created_case = client.post('/api/cases', json={'title': 'Owner Case', 'description': 'x'}, headers={'Authorization': f'Bearer {owner_token}'})
    case_id = created_case.json()['case_id']

    client.post('/api/auth/register', json={'email': 'other@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'other-tenant'})
    other_login = client.post('/api/auth/login', json={'email': 'other@a.com', 'password': 'password123'})
    other_token = other_login.json()['access_token']

    files = {'file': ('doc.txt', b'cannot upload here', 'text/plain')}
    denied = client.post(f'/api/cases/{case_id}/sources/upload', files=files, headers={'Authorization': f'Bearer {other_token}'})
    assert denied.status_code == 404


def test_manual_claim_creation_and_evidence_linkage():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'claim@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-claim'})
    login = client.post('/api/auth/login', json={'email': 'claim@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Claim Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('fact.txt', b'Acme is based in London.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']
    src_id = upload.json()['source_id']

    claim = client.post(f'/api/cases/{case_id}/claims', json={'document_id': doc_id, 'source_id': src_id, 'text': 'Acme is based in London.'}, headers={'Authorization': f'Bearer {token}'})
    assert claim.status_code == 200
    claim_id = claim.json()['claim_id']

    listed = client.get(f'/api/cases/{case_id}/claims', headers={'Authorization': f'Bearer {token}'})
    assert listed.status_code == 200
    assert any(item['claim_id'] == claim_id for item in listed.json())

    evidence = client.get(f'/api/cases/claims/{claim_id}/evidence', headers={'Authorization': f'Bearer {token}'})
    assert evidence.status_code == 200
    assert len(evidence.json()) >= 1


def test_auto_claim_stub_creates_claims_from_chunks():
    import asyncio
    from tasks.document_processing import process_document

    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'autoclaim@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-auto-claim'})
    login = client.post('/api/auth/login', json={'email': 'autoclaim@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Auto Claim Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('fact2.txt', b'Acme is a company. Acme has offices worldwide.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']

    asyncio.run(process_document(doc_id))

    listed = client.get(f'/api/cases/{case_id}/claims', headers={'Authorization': f'Bearer {token}'})
    assert listed.status_code == 200
    auto_claims = [item for item in listed.json() if item['claim_type'] == 'auto_candidate']
    assert len(auto_claims) >= 1


def test_entities_and_relationships_extracted_and_listed():
    import asyncio
    from tasks.document_processing import process_document

    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'entity@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-entity'})
    login = client.post('/api/auth/login', json={'email': 'entity@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Entity Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('ent.txt', b'Alice Smith works with Bob Jones. Acme Corp acquired Beta Corp.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']

    asyncio.run(process_document(doc_id))

    entities = client.get(f'/api/cases/{case_id}/entities', headers={'Authorization': f'Bearer {token}'})
    assert entities.status_code == 200
    assert len(entities.json()) >= 2

    relationships = client.get(f'/api/cases/{case_id}/relationships', headers={'Authorization': f'Bearer {token}'})
    assert relationships.status_code == 200
    assert len(relationships.json()) >= 1


def test_timeline_manual_create_list_and_tenant_scoping():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'tl1@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-tl1'})
    login1 = client.post('/api/auth/login', json={'email': 'tl1@a.com', 'password': 'password123'})
    token1 = login1.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Timeline Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token1}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('tl.txt', b'Event happened on 2026-01-15.', 'text/plain')}, headers={'Authorization': f'Bearer {token1}'})
    source_id = upload.json()['source_id']

    manual = client.post(f'/api/cases/{case_id}/timeline', json={'event_time': '2026-01-16T00:00:00', 'title': 'Manual Event', 'description': 'desc', 'source_id': source_id, 'claim_id': '', 'confidence_score': 0.9}, headers={'Authorization': f'Bearer {token1}'})
    assert manual.status_code == 200

    client.post('/api/auth/register', json={'email': 'tl2@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-tl2'})
    login2 = client.post('/api/auth/login', json={'email': 'tl2@a.com', 'password': 'password123'})
    token2 = login2.json()['access_token']

    denied = client.get(f'/api/cases/{case_id}/timeline', headers={'Authorization': f'Bearer {token2}'})
    assert denied.status_code == 404

    listed = client.get(f'/api/cases/{case_id}/timeline', headers={'Authorization': f'Bearer {token1}'})
    assert listed.status_code == 200
    assert len(listed.json()) >= 1


def test_timeline_generation_from_date_claims():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'tlgen@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-tlgen'})
    login = client.post('/api/auth/login', json={'email': 'tlgen@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Timeline Gen Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('claim.txt', b'Acme signed deal on 2026-02-20.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']
    source_id = upload.json()['source_id']

    claim = client.post(f'/api/cases/{case_id}/claims', json={'document_id': doc_id, 'source_id': source_id, 'text': 'Acme signed deal on 2026-02-20.'}, headers={'Authorization': f'Bearer {token}'})
    assert claim.status_code == 200

    gen = client.post(f'/api/cases/{case_id}/timeline/generate', headers={'Authorization': f'Bearer {token}'})
    assert gen.status_code == 200
    assert gen.json()['created'] >= 1

    listed = client.get(f'/api/cases/{case_id}/timeline', headers={'Authorization': f'Bearer {token}'})
    assert any(item['source_id'] == source_id for item in listed.json())


def test_structured_report_generation_and_markdown_export():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'reporter@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-report'})
    login = client.post('/api/auth/login', json={'email': 'reporter@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    case = client.post('/api/cases', json={'title': 'Report Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('rep.txt', b'Acme signed deal on 2026-03-01. Alice Smith works with Bob Jones.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']
    source_id = upload.json()['source_id']

    claim = client.post(f'/api/cases/{case_id}/claims', json={'document_id': doc_id, 'source_id': source_id, 'text': 'Acme signed deal on 2026-03-01.'}, headers={'Authorization': f'Bearer {token}'})
    assert claim.status_code == 200

    generated = client.post(f'/api/reports/cases/{case_id}/generate', json={'title': 'Case Intelligence Report', 'report_type': 'intelligence'}, headers={'Authorization': f'Bearer {token}'})
    assert generated.status_code == 200
    report = generated.json()
    assert 'executive_summary' in report['content_json']
    assert 'key_findings' in report['content_json']
    assert 'recommended_follow_up_tasks' in report['content_json']
    assert report['content_json']['claims_count'] >= 1

    md = client.get(f"/api/reports/{report['report_id']}/export/markdown", headers={'Authorization': f'Bearer {token}'})
    assert md.status_code == 200
    assert '## Executive Summary' in md.text
    assert '## Claims and Evidence Table' in md.text


def test_watchlist_and_alert_rule_trigger_behavior():
    import asyncio
    from tasks.document_processing import process_document

    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'alert@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-alert'})
    login = client.post('/api/auth/login', json={'email': 'alert@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    wl = client.post('/api/alerts/watchlists', json={'name': 'Fraud Terms', 'terms': ['fraud'], 'entity_ids': [], 'case_id': ''}, headers={'Authorization': f'Bearer {token}'})
    assert wl.status_code == 200

    rule = client.post('/api/alerts/rules', json={'name': 'Keyword Rule', 'scope': 'tenant', 'rule_type': 'keyword_match', 'threshold': 0.0, 'enabled': True, 'metadata_json': {'keywords': ['fraud']}}, headers={'Authorization': f'Bearer {token}'})
    assert rule.status_code == 200

    case = client.post('/api/cases', json={'title': 'Alert Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'})
    case_id = case.json()['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('alert.txt', b'This statement includes fraud indicators and was noted on 2026-04-01.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
    doc_id = upload.json()['document_id']

    asyncio.run(process_document(doc_id))

    alerts = client.get('/api/alerts', headers={'Authorization': f'Bearer {token}'})
    assert alerts.status_code == 200
    assert any('fraud' in a['message'].lower() or 'watchlist' in a['title'].lower() for a in alerts.json())


def test_alerts_are_tenant_scoped():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'a1@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-a1'})
    t1 = client.post('/api/auth/login', json={'email': 'a1@a.com', 'password': 'password123'}).json()['access_token']
    client.post('/api/alerts/rules', json={'name': 'R1', 'scope': 'tenant', 'rule_type': 'risk_score_threshold', 'threshold': 0.2, 'enabled': True, 'metadata_json': {}}, headers={'Authorization': f'Bearer {t1}'})

    client.post('/api/auth/register', json={'email': 'a2@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-a2'})
    t2 = client.post('/api/auth/login', json={'email': 'a2@a.com', 'password': 'password123'}).json()['access_token']

    alerts_other = client.get('/api/alerts', headers={'Authorization': f'Bearer {t2}'})
    assert alerts_other.status_code == 200
    assert len(alerts_other.json()) == 0


def test_panel_run_mock_provider_and_consensus_storage():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'panel@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-panel'})
    token = client.post('/api/auth/login', json={'email': 'panel@a.com', 'password': 'password123'}).json()['access_token']

    case = client.post('/api/cases', json={'title': 'Panel Case', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'}).json()
    case_id = case['case_id']
    upload = client.post(f'/api/cases/{case_id}/sources/upload', files={'file': ('panel.txt', b'Acme reported loss on 2026-03-01.', 'text/plain')}, headers={'Authorization': f'Bearer {token}'}).json()
    client.post(f'/api/cases/{case_id}/claims', json={'document_id': upload['document_id'], 'source_id': upload['source_id'], 'text': 'Acme reported loss on 2026-03-01.'}, headers={'Authorization': f'Bearer {token}'})

    run = client.post(f'/api/cases/{case_id}/panel-runs', json={'prompt': 'Assess financial risk', 'report_id': ''}, headers={'Authorization': f'Bearer {token}'})
    assert run.status_code == 200
    run_id = run.json()['panel_run_id']
    assert 'Consensus is evidence-constrained' in run.json()['consensus_summary']

    responses = client.get(f'/api/cases/panel-runs/{run_id}/responses', headers={'Authorization': f'Bearer {token}'})
    assert responses.status_code == 200
    roles = {r['agent_role'] for r in responses.json()}
    assert roles == {'operator', 'skeptic', 'compliance', 'financial', 'strategic', 'security'}
    assert all(r['response_text'].startswith('MOCK_CHAT:') for r in responses.json())


def test_panel_run_requires_human_approval_before_task_conversion():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'panel2@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-panel2'})
    token = client.post('/api/auth/login', json={'email': 'panel2@a.com', 'password': 'password123'}).json()['access_token']

    case_id = client.post('/api/cases', json={'title': 'Panel Case 2', 'description': 'd'}, headers={'Authorization': f'Bearer {token}'}).json()['case_id']
    run_id = client.post(f'/api/cases/{case_id}/panel-runs', json={'prompt': 'Recommend actions', 'report_id': ''}, headers={'Authorization': f'Bearer {token}'}).json()['panel_run_id']

    approval_req = client.post(f'/api/cases/panel-runs/{run_id}/convert-to-tasks', headers={'Authorization': f'Bearer {token}'})
    assert approval_req.status_code == 200
    approval_id = approval_req.json()['approval_request_id']

    rejected = client.post(f'/api/tasks/approvals/{approval_id}/decision', json={'status': 'rejected'}, headers={'Authorization': f'Bearer {token}'})
    assert rejected.status_code == 200
    assert rejected.json()['created_task'] is None

    approval_req2 = client.post(f'/api/cases/panel-runs/{run_id}/convert-to-tasks', headers={'Authorization': f'Bearer {token}'})
    approval_id2 = approval_req2.json()['approval_request_id']
    approved = client.post(f'/api/tasks/approvals/{approval_id2}/decision', json={'status': 'approved'}, headers={'Authorization': f'Bearer {token}'})
    assert approved.status_code == 200
    assert approved.json()['created_task']['task_id'].startswith('TSK-')


def test_task_create_update_endpoints():
    client = TestClient(app)
    client.post('/api/auth/register', json={'email': 'tasker@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'tenant-task'})
    token = client.post('/api/auth/login', json={'email': 'tasker@a.com', 'password': 'password123'}).json()['access_token']

    created = client.post('/api/tasks', json={'title': 'Review claim', 'description': 'check evidence', 'priority': 'high'}, headers={'Authorization': f'Bearer {token}'})
    assert created.status_code == 200
    task_id = created.json()['task_id']

    updated = client.patch(f'/api/tasks/{task_id}', json={'status': 'approved'}, headers={'Authorization': f'Bearer {token}'})
    assert updated.status_code == 200
    assert updated.json()['status'] == 'approved'


def test_failed_auth_and_authz_are_audited():
    client = TestClient(app)

    unauth = client.get('/api/system/protected')
    assert unauth.status_code == 401

    client.post('/api/auth/register', json={'email': 'auditsec@a.com', 'password': 'password123', 'role': 'admin', 'tenant_id': 'default'})
    login = client.post('/api/auth/login', json={'email': 'auditsec@a.com', 'password': 'password123'})
    token = login.json()['access_token']

    # trigger 403 using non-admin user on admin-only endpoint
    client.post('/api/auth/register', json={'email': 'auditsec-user@a.com', 'password': 'password123', 'role': 'analyst', 'tenant_id': 'default'})
    ulogin = client.post('/api/auth/login', json={'email': 'auditsec-user@a.com', 'password': 'password123'})
    user_token = ulogin.json()['access_token']
    forbidden = client.get('/api/audit', headers={'Authorization': f'Bearer {user_token}'})
    assert forbidden.status_code == 403

    auth_fail_logs = client.get('/api/audit?action=auth.failure', headers={'Authorization': f'Bearer {token}'})
    authz_denied_logs = client.get('/api/audit?action=authz.denied', headers={'Authorization': f'Bearer {token}'})

    assert auth_fail_logs.status_code == 200
    assert authz_denied_logs.status_code == 200
    assert len(auth_fail_logs.json()) >= 1
    assert len(authz_denied_logs.json()) >= 1
