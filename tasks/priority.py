from tasks.queues import QUEUE_MAP

def queue_for(priority: str) -> str:
    return QUEUE_MAP.get(priority, 'default')
