import os

os.environ.setdefault('SECRET_KEY', 'x' * 40)
os.environ.setdefault('LLM_PROVIDER', 'mock')

from llm.gateway import get_provider
from llm.service import extract_claims, extract_entities, panel_response, summarize_document


def test_mock_provider_available_without_external_credentials():
    provider = get_provider()
    assert provider is not None
    assert provider.chat('sys', 'hello').startswith('MOCK_CHAT:')


def test_llm_service_methods_work_with_mock_provider():
    text = 'Acme signed a deal on 2026-01-01. Alice works at Acme.'
    summary = summarize_document(text)
    claims = extract_claims(text)
    entities = extract_entities(text)
    response = panel_response('operator', 'Assess', [{'claim_id': 'CLM-1'}])

    assert summary.startswith('MOCK_CHAT:')
    assert len(claims) >= 1
    assert isinstance(entities, list)
    assert response.startswith('MOCK_CHAT:')
