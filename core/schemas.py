"""Shared Pydantic schemas and enums for SOLACE."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TargetType(str, Enum):
    """Supported investigation target categories."""

    ORGANIZATION = "ORGANIZATION"
    PERSON = "PERSON"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    EVENT = "EVENT"
    THREAT_ACTOR = "THREAT_ACTOR"


class Classification(str, Enum):
    """Traffic Light Protocol classification."""

    WHITE = "TLP:WHITE"
    GREEN = "TLP:GREEN"
    AMBER = "TLP:AMBER"
    RED = "TLP:RED"


class ConfidenceLevel(str, Enum):
    """Analyst confidence levels."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CollectorID(str, Enum):
    """Collector identifiers used across the pipeline."""

    SPIDER_1 = "SPIDER-1"
    SPIDER_2 = "SPIDER-2"
    SPIDER_3 = "SPIDER-3"
    SPIDER_4 = "SPIDER-4"
    SPIDER_5 = "SPIDER-5"
    SPIDER_6 = "SPIDER-6"
    SPIDER_7 = "SPIDER-7"
    SPIDER_8 = "SPIDER-8"
    AGGREGATOR = "AGGREGATOR"
    REPORT_WRITER = "REPORT-WRITER"


class RawIntelItemSchema(BaseModel):
    """Raw normalized intelligence item."""

    content_hash: str
    collector_id: CollectorID
    source_url: str
    source_type: str
    content: str
    content_en: str = ""
    language: str = "en"
    target: str
    target_type: TargetType
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    reliability_score: float = 0.5
    metadata_: dict[str, str] = Field(default_factory=dict)


class CollectionResult(BaseModel):
    """Result wrapper for a collector batch."""

    collector_id: CollectorID
    items: list[RawIntelItemSchema] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
