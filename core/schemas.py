"""Canonical Pydantic v2 schemas for SOLACE."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TargetType(str, Enum):
    person = "person"
    organization = "organization"
    infrastructure = "infrastructure"
    event = "event"
    threat_actor = "threat_actor"
    unknown = "unknown"


class CollectorID(str, Enum):
    seed = "SEED"
    aggregator = "AGGREGATOR"


class RawIntelItemSchema(BaseModel):
    content_hash: str
    collector_id: CollectorID | str
    source_url: str
    source_type: str
    content: str
    target: str
    target_type: TargetType
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    reliability_score: float = Field(default=0.5, ge=0, le=1)
    metadata_: dict[str, Any] = Field(default_factory=dict)


class CollectionResult(BaseModel):
    collector_id: CollectorID | str
    items: list[RawIntelItemSchema] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class ReportSchema(BaseModel):
    report_id: str
    subject: str
    subject_type: str
    classification: str = "TLP:WHITE"
    confidence: str = "MEDIUM"
    confidence_score: float = Field(default=0.5, ge=0, le=1)
    executive_summary: str
    key_findings: list[str] = Field(default_factory=list)
    entity_map: dict[str, Any] = Field(default_factory=dict)
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    behavioral_indicators: list[str] = Field(default_factory=list)
    threat_assessment: dict[str, Any] = Field(default_factory=dict)
    source_log: list[dict[str, Any]] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    analyst_notes: list[str] = Field(default_factory=list)
    full_markdown: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PipelineRequest(BaseModel):
    target: str = Field(min_length=1)
    target_type: TargetType = TargetType.unknown
    tenant_id: str | None = None


class PipelineResponse(BaseModel):
    job_id: str
    report_id: str
    status: str
    raw_count: int
    enriched_count: int
    entity_count: int
    panel_session_id: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(LoginRequest):
    tenant_id: str = "default"
    role: str = "analyst"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FullTokenResponse(TokenResponse):
    refresh_token: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str


class CaseCreateRequest(BaseModel):
    title: str
    description: str = ""


class WatchCreateRequest(BaseModel):
    target: str
    target_type: TargetType = TargetType.unknown
    cadence: str = "daily"


class TenantCreateRequest(BaseModel):
    tenant_id: str
    name: str


class EntitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    entity_id: str
    tenant_id: str = "default"
    name: str
    normalized_name: str
    entity_type: str
    confidence_score: float = 0.5
    attributes: dict[str, Any] = Field(default_factory=dict)
    source_report_ids: list[str] = Field(default_factory=list)


class SearchRequest(BaseModel):
    q: str
    limit: int = Field(default=20, ge=1, le=100)


class SearchResultSchema(BaseModel):
    id: str
    type: str
    title: str
    snippet: str
    score: float = 1.0


# ─── Panel types ─────────────────────────────────────────────────────────────

class PanelStatus(str, Enum):
    ACTIVE = "active"
    COMPLETE = "complete"
    FAILED = "failed"


class AnalystID(str, Enum):
    ALPHA = "ANALYST-ALPHA"
    BRAVO = "ANALYST-BRAVO"
    DIRECTOR = "SESSION-DIRECTOR"


class PanelTurn(BaseModel):
    analyst: AnalystID
    content: str
    round_number: int = 0
    is_loop_flagged: bool = False


class Disagreement(BaseModel):
    round_number: int
    topic: str
    alpha_position: str
    bravo_position: str


# ─── Tenant schemas ───────────────────────────────────────────────────────────

class TenantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tenant_id: str
    name: str
    status: str = "active"
    settings: dict[str, Any] = Field(default_factory=dict)


# ─── Autonomous task schemas ──────────────────────────────────────────────────

class AutonomousTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_id: str
    tenant_id: str
    report_id: str | None = None
    title: str
    description: str = ""
    priority: str = "default"
    status: str = "open"


# ─── Classification / confidence enums ───────────────────────────────────────

class Classification(str, Enum):
    WHITE = "TLP:WHITE"
    GREEN = "TLP:GREEN"
    AMBER = "TLP:AMBER"
    RED = "TLP:RED"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
