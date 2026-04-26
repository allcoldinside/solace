def aggregate(items: list[dict]) -> list[dict]:
    seen = set(); out = []
    for i in items:
        key = i.get('content', '')
        if key in seen:
            continue
        seen.add(key); out.append(i)
    return out
