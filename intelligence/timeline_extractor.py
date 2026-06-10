import re
from datetime import datetime

DATE_PATTERNS = [
    re.compile(r'\b(\d{4}-\d{2}-\d{2})\b'),
    re.compile(r'\b([A-Z][a-z]+\s+\d{1,2},\s+\d{4})\b'),
]


def extract_timeline_candidates(claim_text: str) -> list[dict]:
    candidates = []
    for pattern in DATE_PATTERNS:
        for match in pattern.findall(claim_text):
            try:
                if '-' in match:
                    dt = datetime.strptime(match, '%Y-%m-%d')
                else:
                    dt = datetime.strptime(match, '%B %d, %Y')
            except ValueError:
                continue
            candidates.append({'event_time': dt, 'title': 'Claim-derived event', 'description': claim_text})
    return candidates
