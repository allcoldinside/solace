import re
from html import unescape


def extract_text(content: bytes, filename: str, mime_type: str | None) -> str:
    lower_name = filename.lower()
    mt = (mime_type or '').lower()

    if lower_name.endswith(('.txt', '.md')) or mt.startswith('text/plain'):
        return content.decode('utf-8', errors='ignore')

    if lower_name.endswith('.html') or mt.startswith('text/html'):
        raw = content.decode('utf-8', errors='ignore')
        no_tags = re.sub(r'<[^>]+>', ' ', raw)
        return unescape(re.sub(r'\s+', ' ', no_tags)).strip()

    if lower_name.endswith('.pdf') or mt == 'application/pdf':
        return '[pdf text extraction stub: parser not configured]'

    return '[unsupported text extraction type]'
