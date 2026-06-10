from llm.gateway import get_provider
from llm.templates.prompts import PROMPTS


def summarize_document(text: str) -> str:
    provider = get_provider()
    return provider.chat(PROMPTS['summarize_document'], text)


def extract_claims(text: str) -> list[dict]:
    provider = get_provider()
    return provider.extract(text, mode='claims')


def extract_entities(text: str) -> list[dict]:
    provider = get_provider()
    return provider.extract(text, mode='entities')


def panel_response(role: str, prompt: str, claims: list[dict]) -> str:
    provider = get_provider()
    claim_refs = ', '.join(c.get('claim_id', 'unknown') for c in claims[:3])
    return provider.chat(PROMPTS['panel_response'], f'Role={role}; Prompt={prompt}; ClaimRefs={claim_refs}')
