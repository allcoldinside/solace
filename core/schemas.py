from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TargetType(str, Enum):
    organization = 'organization'
    person = 'person'
    infrastructure = 'infrastructure'
    event = 'event'


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
