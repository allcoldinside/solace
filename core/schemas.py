from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator


class TargetType(str, Enum):
    organization = 'organization'
    person = 'person'
    infrastructure = 'infrastructure'
    event = 'event'


# ---------------------------------------------------------------------------
# Collector schemas
# ---------------------------------------------------------------------------

class CollectorID(str, Enum):
    SEED = 'seed'
    SPIDER_9 = 'SPIDER-9'
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
    UNKNOWN = 'unknown'

    @classmethod
    def _missing_(cls, value: object) -> 'CollectorID':
        obj = str.__new__(cls, value)
        obj._name_ = str(value)
        obj._value_ = str(value)
        return obj


class RawIntelItemSchema(BaseModel):
    content_hash: str
    collector_id: CollectorID
    source_url: str
    source_type: str
    content: str
    target: str
    target_type: TargetType
    collected_at: datetime
    reliability_score: float = 0.5
    metadata_: dict = Field(default_factory=dict)


class CollectionResult(BaseModel):
    collector_id: CollectorID
    items: list[RawIntelItemSchema] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# API / pipeline schemas
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
    target: str = Field(min_length=1, max_length=512)
    target_type: TargetType = TargetType.organization

    @field_validator('target')
    @classmethod
    def target_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('target must not be blank')
        return v.strip()


class PipelineResponse(BaseModel):
    report_id: str
    session_id: str
    entities_saved: int
    status: str = 'ok'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
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


class CaseCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=512)
    description: str = ''


class WatchCreateRequest(BaseModel):
    target: str = Field(min_length=1, max_length=512)
    target_type: TargetType


class TenantCreateRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)


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
