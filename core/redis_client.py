"""Redis client helper."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from config.settings import get_settings


@lru_cache(maxsize=1)
def get_redis() -> Any:
    try:
        from redis.asyncio import Redis
        return Redis.from_url(get_settings().redis_url, decode_responses=True)
    except Exception:
        return None
