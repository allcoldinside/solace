from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Tenant(Base):
    __tablename__ = 'tenants'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default='analyst')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)




class UserTenantMembership(Base):
    __tablename__ = 'user_tenant_memberships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    role: Mapped[str] = mapped_column(String(32), default='analyst')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = 'reports'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    subject: Mapped[str] = mapped_column(String(255), index=True)
    subject_type: Mapped[str] = mapped_column(String(64))
    classification: Mapped[str] = mapped_column(String(32))
    confidence: Mapped[str] = mapped_column(String(32))
    confidence_score: Mapped[float] = mapped_column(Float)
    full_markdown: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    title: Mapped[str] = mapped_column(String(255), default='')
    report_type: Mapped[str] = mapped_column(String(64), default='case_summary')
    status: Mapped[str] = mapped_column(String(32), default='draft')
    generated_by: Mapped[str] = mapped_column(String(64), default='system')
    content_markdown: Mapped[str] = mapped_column(Text, default='')
    content_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PanelSessionRecord(Base):
    __tablename__ = 'panel_sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    report_id: Mapped[str] = mapped_column(String(64), index=True)
    summary: Mapped[str] = mapped_column(Text, default='')
    transcript: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Case(Base):
    __tablename__ = 'cases'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    status: Mapped[str] = mapped_column(String(32), default='open')
    priority: Mapped[str] = mapped_column(String(16), default='medium')
    created_by: Mapped[str] = mapped_column(String(64), default='system')
    assigned_to: Mapped[str] = mapped_column(String(64), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class WatchRecord(Base):
    __tablename__ = 'watches'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    watch_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    target_type: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    actor_user_id: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_id: Mapped[str] = mapped_column(String(128), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    request_id: Mapped[str] = mapped_column(String(128), index=True)
    ip_address: Mapped[str] = mapped_column(String(64), default='unknown')
    user_agent: Mapped[str] = mapped_column(String(512), default='unknown')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MemoryEntry(Base):
    __tablename__ = 'memory_entries'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    report_id: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AutonomousTask(Base):
    __tablename__ = 'autonomous_tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    task_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    report_id: Mapped[str] = mapped_column(String(64), index=True)
    kind: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default='queued')
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    title: Mapped[str] = mapped_column(String(255), default='')
    report_type: Mapped[str] = mapped_column(String(64), default='case_summary')
    status: Mapped[str] = mapped_column(String(32), default='draft')
    generated_by: Mapped[str] = mapped_column(String(64), default='system')
    content_markdown: Mapped[str] = mapped_column(Text, default='')
    content_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Entity(Base):
    __tablename__ = 'entities'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    entity_type: Mapped[str] = mapped_column(String(64), index=True, default='unknown')
    canonical_name: Mapped[str] = mapped_column(String(255), index=True)
    aliases: Mapped[list] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CollectionJob(Base):
    __tablename__ = 'collection_jobs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(32), default='done')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


Index('ix_entities_tenant_name', Entity.tenant_id, Entity.canonical_name)


Index('ix_user_tenant_memberships_user_tenant', UserTenantMembership.user_id, UserTenantMembership.tenant_id, unique=True)


class Source(Base):
    __tablename__ = 'sources'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    source_type: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(255))
    uri: Mapped[str] = mapped_column(String(1024), default='')
    collection_method: Mapped[str] = mapped_column(String(64))
    authorization_basis: Mapped[str] = mapped_column(String(255), default='')
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    collected_by: Mapped[str] = mapped_column(String(64))
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(128))
    object_key: Mapped[str] = mapped_column(String(255), unique=True)
    sha256_hash: Mapped[str] = mapped_column(String(64), index=True)
    size_bytes: Mapped[int] = mapped_column(Integer)
    text_content: Mapped[str] = mapped_column(Text, default='')
    processing_status: Mapped[str] = mapped_column(String(32), default='pending')
    processing_error: Mapped[str] = mapped_column(Text, default='')
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    document_id: Mapped[str] = mapped_column(String(64), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    start_offset: Mapped[int] = mapped_column(Integer)
    end_offset: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Claim(Base):
    __tablename__ = 'claims'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    document_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    text: Mapped[str] = mapped_column(Text)
    normalized_text: Mapped[str] = mapped_column(Text)
    claim_type: Mapped[str] = mapped_column(String(64), default='factual_statement')
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    verification_status: Mapped[str] = mapped_column(String(32), default='unverified')
    created_by: Mapped[str] = mapped_column(String(64), default='system')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class EvidenceItem(Base):
    __tablename__ = 'evidence_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    claim_id: Mapped[str] = mapped_column(String(64), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    document_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    chunk_id: Mapped[str] = mapped_column(String(64), index=True)
    start_offset: Mapped[int] = mapped_column(Integer)
    end_offset: Mapped[int] = mapped_column(Integer)
    excerpt_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class EntityRelationship(Base):
    __tablename__ = 'entity_relationships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    relationship_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    subject_entity_id: Mapped[str] = mapped_column(String(64), index=True)
    predicate: Mapped[str] = mapped_column(String(128))
    object_entity_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    claim_id: Mapped[str] = mapped_column(String(64), index=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class TimelineEntry(Base):
    __tablename__ = 'timeline_entries'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timeline_entry_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    event_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default='')
    source_id: Mapped[str] = mapped_column(String(64), index=True)
    claim_id: Mapped[str] = mapped_column(String(64), index=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Watchlist(Base):
    __tablename__ = 'watchlists'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    watchlist_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    name: Mapped[str] = mapped_column(String(255))
    terms: Mapped[list] = mapped_column(JSON, default=list)
    entity_ids: Mapped[list] = mapped_column(JSON, default=list)
    created_by: Mapped[str] = mapped_column(String(64), default='system')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AlertRule(Base):
    __tablename__ = 'alert_rules'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    scope: Mapped[str] = mapped_column(String(64), default='tenant')
    rule_type: Mapped[str] = mapped_column(String(64))
    threshold: Mapped[float] = mapped_column(Float, default=0.0)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alert_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    rule_id: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(32), default='warning')
    message: Mapped[str] = mapped_column(Text)
    source_id: Mapped[str] = mapped_column(String(64), default='')
    claim_id: Mapped[str] = mapped_column(String(64), default='')
    status: Mapped[str] = mapped_column(String(32), default='new')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class PanelRun(Base):
    __tablename__ = 'panel_runs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    panel_run_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True)
    report_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    status: Mapped[str] = mapped_column(String(32), default='completed')
    prompt: Mapped[str] = mapped_column(Text)
    consensus_summary: Mapped[str] = mapped_column(Text, default='')
    created_by: Mapped[str] = mapped_column(String(64), default='system')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AgentResponse(Base):
    __tablename__ = 'agent_responses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_response_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    panel_run_id: Mapped[str] = mapped_column(String(64), index=True)
    agent_role: Mapped[str] = mapped_column(String(64), index=True)
    response_text: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    concerns_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    case_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default='')
    status: Mapped[str] = mapped_column(String(32), default='pending')
    priority: Mapped[str] = mapped_column(String(32), default='medium')
    assigned_to: Mapped[str] = mapped_column(String(64), default='')
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    source_type: Mapped[str] = mapped_column(String(64), default='manual')
    source_id: Mapped[str] = mapped_column(String(64), default='')
    created_by: Mapped[str] = mapped_column(String(64), default='system')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ApprovalRequest(Base):
    __tablename__ = 'approval_requests'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approval_request_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    requested_action: Mapped[str] = mapped_column(String(128))
    target_type: Mapped[str] = mapped_column(String(64))
    target_id: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default='pending')
    requested_by: Mapped[str] = mapped_column(String(64))
    approved_by: Mapped[str] = mapped_column(String(64), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
