def enrich_items(items: list[dict]) -> list[dict]:
    for i in items:
        i['enriched'] = True
        i['tokens'] = i.get('content', '').split()
    return items
