import uuid


def generate_autonomous_tasks(report_id: str) -> list[dict]:
    return [{'task_id': f'TASK-{uuid.uuid4().hex[:10]}', 'report_id': report_id, 'kind': 'follow-up-collection'}]
