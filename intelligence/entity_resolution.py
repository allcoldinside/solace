import re


ORG_HINTS = {'inc', 'corp', 'ltd', 'llc', 'org'}


def extract_candidates(text: str) -> list[dict]:
    words = re.findall(r'[A-Z][a-zA-Z0-9]+', text)
    out = []
    for w in words:
        kind = 'organization' if w.lower() in ORG_HINTS else 'entity'
        out.append({'name': w, 'kind': kind, 'confidence': 0.6})
    return out


def resolve_entities(items: list[dict]) -> list[dict]:
    merged: dict[tuple[str, str], dict] = {}
    for i in items:
        for c in extract_candidates(i.get('content', '')):
            k = (c['name'], c['kind'])
            merged[k] = c
    return list(merged.values())
