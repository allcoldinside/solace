"""Base collector utilities for SOLACE spider bots."""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

import aiohttp

from core.schemas import CollectionResult, CollectorID, RawIntelItemSchema, TargetType

logger = logging.getLogger(__name__)


class BaseCollector:
    """Base class for asynchronous SOLACE collectors.

    Subclasses should set class attributes and implement ``collect``.
    """

    bot_id: str = "SPIDER-0"
    domain: str = "generic"
    rate_limit: float = 1.0
    source_reliability: float = 0.5

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        return CollectionResult(collector_id=CollectorID(self.bot_id), items=[])

    async def fetch_json(
        self,
        session: aiohttp.ClientSession,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | None:
        try:
            async with session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=20)) as response:
                if response.status >= 400:
                    logger.warning("http_error url=%s status=%d", url, response.status)
                    return None
                return await response.json(content_type=None)
        except aiohttp.ClientError as error:
            logger.warning("network_error url=%s error=%s", url, error)
            return None

    async def fetch_text(
        self,
        session: aiohttp.ClientSession,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> str:
        try:
            async with session.get(url, headers=headers, params=params, timeout=aiohttp.ClientTimeout(total=20)) as response:
                if response.status >= 400:
                    logger.warning("http_error url=%s status=%d", url, response.status)
                    return ""
                return await response.text()
        except aiohttp.ClientError as error:
            logger.warning("network_error url=%s error=%s", url, error)
            return ""

    def build_item(
        self,
        *,
        source_url: str,
        source_type: str,
        content: str,
        target: str,
        target_type: TargetType,
        reliability: float | None = None,
        metadata: dict[str, str] | None = None,
    ) -> RawIntelItemSchema:
        content_hash = hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()
        return RawIntelItemSchema(
            content_hash=content_hash,
            collector_id=CollectorID(self.bot_id),
            source_url=source_url,
            source_type=source_type,
            content=content,
            target=target,
            target_type=target_type,
            collected_at=datetime.now(timezone.utc),
            reliability_score=reliability if reliability is not None else self.source_reliability,
            metadata_=metadata or {},
        )
