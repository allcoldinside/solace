"""Base collector utilities for SOLACE spider bots."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

import aiohttp
import structlog

from core.schemas import CollectionResult, CollectorID, RawIntelItemSchema, TargetType


class BaseCollector:
    """Base class for asynchronous SOLACE collectors.

    Subclasses should set class attributes and implement ``collect``.
    """

    bot_id: str = "SPIDER-0"
    domain: str = "generic"
    rate_limit: float = 1.0
    source_reliability: float = 0.5

    def __init__(self) -> None:
        """Initialize base collector logger."""
        self.logger = structlog.get_logger(component=self.bot_id, domain=self.domain)

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect raw intelligence for target.

        Args:
            target: Investigation target.
            target_type: Target category.

        Returns:
            Collection result payload.
        """
        return CollectionResult(collector_id=CollectorID(self.bot_id), items=[])

    async def fetch_json(
        self,
        session: aiohttp.ClientSession,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | None:
        """Fetch JSON content from URL with error handling."""
        try:
            async with session.get(url, headers=headers, params=params, timeout=20) as response:
                if response.status >= 400:
                    self.logger.warning("http_error", url=url, status=response.status)
                    return None
                return await response.json(content_type=None)
        except aiohttp.ClientError as error:
            self.logger.warning("network_error", url=url, error=str(error))
            return None

    async def fetch_text(
        self,
        session: aiohttp.ClientSession,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> str:
        """Fetch plain text response with resilient handling."""
        try:
            async with session.get(url, headers=headers, params=params, timeout=20) as response:
                if response.status >= 400:
                    self.logger.warning("http_error", url=url, status=response.status)
                    return ""
                return await response.text()
        except aiohttp.ClientError as error:
            self.logger.warning("network_error", url=url, error=str(error))
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
        """Build normalized item schema object."""
        content_hash = hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()
        return RawIntelItemSchema(
            content_hash=content_hash,
            collector_id=CollectorID(self.bot_id),
            source_url=source_url,
            source_type=source_type,
            content=content,
            target=target,
            target_type=target_type,
            collected_at=datetime.utcnow(),
            reliability_score=reliability if reliability is not None else self.source_reliability,
            metadata_=metadata or {},
        )
