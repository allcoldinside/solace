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



class CaseStatus(str, Enum):
    open = 'open'
    active = 'active'
    paused = 'paused'
    closed = 'closed'
    archived = 'archived'


class CaseCreateRequest(BaseModel):
    title: str
    description: str = ''
    priority: str = 'medium'
    assigned_to: str = ''


class CaseUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: CaseStatus | None = None
    priority: str | None = None
    assigned_to: str | None = None


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



class VerificationStatus(str, Enum):
    unverified = 'unverified'
    supported = 'supported'
    contradicted = 'contradicted'
    disputed = 'disputed'
    resolved = 'resolved'


class ClaimCreateRequest(BaseModel):
    document_id: str
    source_id: str
    text: str
    claim_type: str = 'factual_statement'
    confidence_score: float = 0.8
    verification_status: VerificationStatus = VerificationStatus.unverified
    metadata_json: dict = Field(default_factory=dict)


class ClaimUpdateRequest(BaseModel):
    verification_status: VerificationStatus | None = None
    confidence_score: float | None = None
    metadata_json: dict | None = None



class TimelineEntryCreateRequest(BaseModel):
    event_time: datetime
    title: str
    description: str = ''
    source_id: str
    claim_id: str = ''
    confidence_score: float = 0.8
    metadata_json: dict = Field(default_factory=dict)



class ReportGenerateRequest(BaseModel):
    title: str
    report_type: str = 'intelligence'



class WatchlistCreateRequest(BaseModel):
    name: str
    terms: list[str] = Field(default_factory=list)
    entity_ids: list[str] = Field(default_factory=list)
    case_id: str = ''


class AlertRuleCreateRequest(BaseModel):
    name: str
    scope: str = 'tenant'
    rule_type: str
    threshold: float = 0.0
    enabled: bool = True
    metadata_json: dict = Field(default_factory=dict)


class AlertRuleUpdateRequest(BaseModel):
    threshold: float | None = None
    enabled: bool | None = None
    metadata_json: dict | None = None



class PanelRunCreateRequest(BaseModel):
    prompt: str
    report_id: str = ''


class PanelApproveRequest(BaseModel):
    approved: bool



class TaskCreateRequest(BaseModel):
    case_id: str = ''
    title: str
    description: str = ''
    priority: str = 'medium'
    assigned_to: str = ''
    due_at: datetime | None = None
    source_type: str = 'manual'
    source_id: str = ''


class TaskUpdateRequest(BaseModel):
    status: str | None = None
    priority: str | None = None
    assigned_to: str | None = None
    due_at: datetime | None = None


class ApprovalDecisionRequest(BaseModel):
    status: str
