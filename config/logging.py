import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        if hasattr(record, 'trace_id'):
            payload['trace_id'] = record.trace_id
        return json.dumps(payload)


def configure_logging(level: str = 'INFO') -> None:
    root = logging.getLogger()
    root.handlers.clear()
    h = logging.StreamHandler()
    h.setFormatter(JsonFormatter())
    root.addHandler(h)
    root.setLevel(level)
