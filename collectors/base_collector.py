"""Base async collector for SOLACE collectors."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from typing import Any

from core.schemas import CollectionResult, RawIntelItemSchema, TargetType


class BaseCollector(ABC):
    collector_id: str = "BASE"

    def _content_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _build_item(self, *, source_url: str, source_type: str, content: str, target: str, target_type: TargetType, reliability_score: float = 0.5, metadata_: dict[str, Any] | None = None) -> RawIntelItemSchema:
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
        return CollectionResult(collector_id=self.collector_id, items=items, errors=errors or [])

    @abstractmethod
    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        raise NotImplementedError
