import re


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def clean_html(text: str) -> str:
    without_tags = re.sub(r'<[^>]+>', ' ', text)
    return normalize_whitespace(without_tags)


def chunk_text(text: str, chunk_size: int = 500) -> list[dict]:
    chunks: list[dict] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append({'chunk_index': index, 'start_offset': start, 'end_offset': end, 'text': chunk})
        start = end
        index += 1
    return chunks
