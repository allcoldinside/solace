import re

ENTITY_PATTERNS = {
    'email': re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b'),
    'phone': re.compile(r'\b\+?\d[\d\-\s]{7,}\d\b'),
    'domain': re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'),
}


def infer_type(token: str) -> str:
    if '@' in token:
        return 'email'
    if re.match(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$', token):
        return 'domain'
    if any(ch.isdigit() for ch in token) and len(token) >= 8:
        return 'phone'
    if token.istitle() and ' ' in token:
        return 'person'
    if token.lower().endswith(('inc', 'corp', 'ltd', 'llc')):
        return 'organization'
    return 'unknown'


def extract_entities(text: str) -> list[dict]:
    found = []
    for etype, pattern in ENTITY_PATTERNS.items():
        for match in pattern.findall(text):
            found.append({'canonical_name': match, 'entity_type': etype, 'confidence_score': 0.8, 'aliases': []})

    # basic title-cased multi-word candidates
    for m in re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text):
        found.append({'canonical_name': m, 'entity_type': infer_type(m), 'confidence_score': 0.6, 'aliases': []})

    # de-dup raw candidates
    uniq = {}
    for item in found:
        key = item['canonical_name'].lower()
        uniq[key] = item
    return list(uniq.values())


def extract_relationship_candidates(text: str) -> list[tuple[str, str, str]]:
    relationships = []
    for sentence in text.split('.'):
        s = sentence.strip()
        if ' acquired ' in s.lower():
            parts = re.split(r' acquired ', s, flags=re.IGNORECASE)
            if len(parts) == 2:
                relationships.append((parts[0].strip(), 'acquired', parts[1].strip()))
        if ' works with ' in s.lower():
            parts = re.split(r' works with ', s, flags=re.IGNORECASE)
            if len(parts) == 2:
                relationships.append((parts[0].strip(), 'works_with', parts[1].strip()))
    return relationships
