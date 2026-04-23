"""Base async collector for SOLACE spiders."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
import hashlib
import time
from typing import Any

import aiohttp

from core.schemas import CollectionResult, CollectorID, RawIntelItemSchema, TargetType


class BaseCollector(ABC):
    """Abstract collector implementing shared async HTTP behavior."""

    collector_id: CollectorID

    def __init__(self, collector_id: CollectorID, requests_per_second: float = 1.0) -> None:
        """Initialize a collector.

        Args:
            collector_id: Unique collector identity.
            requests_per_second: API throttle rate.
        """
        self.collector_id = collector_id
        self.requests_per_second = max(requests_per_second, 0.1)
        self._session: aiohttp.ClientSession | None = None
        self._last_request_ts: float = 0.0

    async def __aenter__(self) -> "BaseCollector":
        timeout = aiohttp.ClientTimeout(total=30)
        self._session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _enforce_rate_limit(self) -> None:
        """Sleep when needed to honor max request rate."""
        interval = 1.0 / self.requests_per_second
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < interval:
            await asyncio.sleep(interval - elapsed)

    async def _fetch(self, url: str, headers: dict[str, str] | None = None) -> str:
        """Fetch URL body with retry and backoff behavior."""
        if self._session is None:
            raise RuntimeError("Collector session not initialized. Use async context manager.")

        backoff = 0.5
        last_error: Exception | None = None
        for attempt in range(3):
            await self._enforce_rate_limit()
            self._last_request_ts = time.monotonic()
            try:
                async with self._session.get(url, headers=headers) as response:
                    if response.status == 429:
                        retry_after = response.headers.get("Retry-After")
                        delay = float(retry_after) if retry_after and retry_after.isdigit() else backoff
                        await asyncio.sleep(delay)
                        backoff *= 2
                        continue
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientResponseError as error:
                last_error = error
                if error.status and 400 <= error.status < 500 and error.status != 429:
                    raise
            except (aiohttp.ClientError, asyncio.TimeoutError) as error:
                last_error = error
            await asyncio.sleep(backoff)
            backoff *= 2
        if last_error is not None:
            raise last_error
        raise RuntimeError("Fetch failed without concrete error.")

    def _content_hash(self, content: str) -> str:
        """Generate deterministic SHA-256 hash for content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _build_item(
        self,
        *,
        source_url: str,
        source_type: str,
        content: str,
        target: str,
        target_type: TargetType,
        reliability_score: float,
        metadata_: dict[str, str] | None = None,
    ) -> RawIntelItemSchema:
        """Build a normalized raw item from collector output."""
        return RawIntelItemSchema(
            content_hash=self._content_hash(content),
            collector_id=self.collector_id,
            source_url=source_url,
            source_type=source_type,
            content=content,
            target=target,
            target_type=target_type,
            reliability_score=max(0.0, min(1.0, reliability_score)),
            metadata_=metadata_ or {},
        )

    def _build_result(self, items: list[RawIntelItemSchema], errors: list[str] | None = None) -> CollectionResult:
        """Build a collection result payload."""
        return CollectionResult(collector_id=self.collector_id, items=items, errors=errors or [])

    @abstractmethod
    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect intel for target.

        Args:
            target: Investigation target.
            target_type: Investigation target classification.

        Returns:
            Collection result with normalized items.
        """
