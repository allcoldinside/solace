def ingest_graph(entities: list[dict], report_id: str) -> dict:
    return {'nodes': len(entities), 'edges': max(0, len(entities)-1), 'report_id': report_id}
