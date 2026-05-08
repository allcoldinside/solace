from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Core enumerations
# ---------------------------------------------------------------------------

class TargetType(str, Enum):
    organization = 'organization'
    person = 'person'
    infrastructure = 'infrastructure'
    event = 'event'


class ClassificationLevel(str, Enum):
    tlp_white = 'TLP:WHITE'
    tlp_green = 'TLP:GREEN'
    tlp_amber = 'TLP:AMBER'
    tlp_red = 'TLP:RED'


class ConfidenceLevel(str, Enum):
    low = 'LOW'
    medium = 'MEDIUM'
    high = 'HIGH'
    confirmed = 'CONFIRMED'


class PanelStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    CONCLUDED = 'CONCLUDED'
    ERROR = 'ERROR'


class AnalystID(str, Enum):
    ALPHA = 'ANALYST-ALPHA'
    BRAVO = 'ANALYST-BRAVO'
    DIRECTOR = 'SESSION-DIRECTOR'
    GAMMA = 'ANALYST-GAMMA'
    DELTA = 'ANALYST-DELTA'


class CollectorID(str, Enum):
    SEED = 'SEED'
    SPIDER_01 = 'SPIDER-01'
    SPIDER_02 = 'SPIDER-02'
    SPIDER_03 = 'SPIDER-03'
    SPIDER_04 = 'SPIDER-04'
    SPIDER_05 = 'SPIDER-05'
    SPIDER_06 = 'SPIDER-06'
    SPIDER_07 = 'SPIDER-07'
    SPIDER_08 = 'SPIDER-08'
    SPIDER_09 = 'SPIDER-09'
    SPIDER_10 = 'SPIDER-10'
    SPIDER_11 = 'SPIDER-11'
    SPIDER_12 = 'SPIDER-12'
    SPIDER_13 = 'SPIDER-13'
    SPIDER_14 = 'SPIDER-14'
    SPIDER_15 = 'SPIDER-15'
    SPIDER_16 = 'SPIDER-16'
    SPIDER_17 = 'SPIDER-17'
    SPIDER_18 = 'SPIDER-18'
    SPIDER_19 = 'SPIDER-19'
    SPIDER_20 = 'SPIDER-20'
    SPIDER_21 = 'SPIDER-21'
    SPIDER_22 = 'SPIDER-22'
    SPIDER_23 = 'SPIDER-23'
    SPIDER_24 = 'SPIDER-24'


# ---------------------------------------------------------------------------
# Collector schemas
# ---------------------------------------------------------------------------

class RawIntelItemSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content_hash: str
    collector_id: CollectorID
    source_url: str
    source_type: str
    content: str
    target: str
    target_type: TargetType
    collected_at: datetime
    reliability_score: float = 0.5
    metadata_: dict[str, str] = Field(default_factory=dict, alias='metadata')


class CollectionResult(BaseModel):
    collector_id: CollectorID
    items: list[RawIntelItemSchema] = Field(default_factory=list)
    error: str | None = None


# ---------------------------------------------------------------------------
# Panel schemas
# ---------------------------------------------------------------------------

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


class PanelSessionSchema(BaseModel):
    session_id: str
    report_id: str
    summary: str
    transcript: list[Any] = Field(default_factory=list)
    created_at: datetime | None = None


# ---------------------------------------------------------------------------
# Report / pipeline schemas
# ---------------------------------------------------------------------------

class ReportSchema(BaseModel):
    report_id: str
    subject: str
    subject_type: str
    classification: str
    confidence: str
    confidence_score: float
    full_markdown: str
    created_at: datetime | None = None


class PipelineRequest(BaseModel):
    target: str
    target_type: TargetType = TargetType.organization


class PipelineResponse(BaseModel):
    report_id: str
    session_id: str
    entities_saved: int
    status: str = 'ok'


# ---------------------------------------------------------------------------
# Auth schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    role: str = 'analyst'
    tenant_id: str = 'default'


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class FullTokenResponse(TokenResponse):
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str


# ---------------------------------------------------------------------------
# Resource schemas
# ---------------------------------------------------------------------------

class CaseCreateRequest(BaseModel):
    title: str
    description: str = ''


class WatchCreateRequest(BaseModel):
    target: str
    target_type: TargetType


class TenantCreateRequest(BaseModel):
    tenant_id: str
    name: str


class EntitySchema(BaseModel):
    entity_id: str
    name: str
    kind: str
    confidence: float


class SearchRequest(BaseModel):
    q: str


class SearchResultSchema(BaseModel):
    kind: str
    id: str
    title: str
    score: float
