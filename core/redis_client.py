from __future__ import annotations

import logging
import redis.asyncio as aioredis
from functools import lru_cache
from config.settings import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_client() -> aioredis.Redis:
    return aioredis.from_url(get_settings().redis_url, decode_responses=True)


def get_redis_url() -> str:
    return get_settings().redis_url


async def cache_get(key: str) -> str | None:
    try:
        return await _get_client().get(key)
    except Exception as exc:
        logger.debug("redis cache_get miss key=%s err=%s", key, exc)
        return None


async def cache_set(key: str, value: str, ex: int = 300) -> None:
    try:
        await _get_client().set(key, value, ex=ex)
    except Exception as exc:
        logger.debug("redis cache_set failed key=%s err=%s", key, exc)


async def cache_delete(key: str) -> None:
    try:
        await _get_client().delete(key)
    except Exception as exc:
        logger.debug("redis cache_delete failed key=%s err=%s", key, exc)
