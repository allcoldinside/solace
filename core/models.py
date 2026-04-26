"""Canonical SQLAlchemy 2.0 ORM models for SOLACE."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


def public_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("USER"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(64), default="analyst", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active")
    settings: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Report(Base, TimestampMixin):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[str] = mapped_column(String(96), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    subject: Mapped[str] = mapped_column(String(255), index=True)
    subject_type: Mapped[str] = mapped_column(String(64), index=True)
    classification: Mapped[str] = mapped_column(String(32), default="TLP:WHITE")
    confidence: Mapped[str] = mapped_column(String(32), default="MEDIUM")
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    executive_summary: Mapped[str] = mapped_column(Text)
    key_findings: Mapped[list[Any]] = mapped_column(JSON, default=list)
    entity_map: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    timeline: Mapped[list[Any]] = mapped_column(JSON, default=list)
    behavioral_indicators: Mapped[list[Any]] = mapped_column(JSON, default=list)
    threat_assessment: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    source_log: Mapped[list[Any]] = mapped_column(JSON, default=list)
    gaps: Mapped[list[Any]] = mapped_column(JSON, default=list)
    analyst_notes: Mapped[list[Any]] = mapped_column(JSON, default=list)
    full_markdown: Mapped[str] = mapped_column(Text)


class PanelSessionRecord(Base, TimestampMixin):
    __tablename__ = "panel_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(96), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    report_id: Mapped[str] = mapped_column(String(96), index=True)
    status: Mapped[str] = mapped_column(String(32), default="complete")
    transcript: Mapped[list[Any]] = mapped_column(JSON, default=list)
    synthesis: Mapped[str] = mapped_column(Text, default="")


class Case(Base, TimestampMixin):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("CASE"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="open")


class WatchRecord(Base, TimestampMixin):
    __tablename__ = "watches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    watch_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("WATCH"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    target_type: Mapped[str] = mapped_column(String(64), default="unknown")
    cadence: Mapped[str] = mapped_column(String(32), default="daily")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("AUDIT"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    actor_user_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class RevokedToken(Base, TimestampMixin):
    __tablename__ = "revoked_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MemoryEntry(Base, TimestampMixin):
    __tablename__ = "memory_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    memory_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("MEM"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    report_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[Any]] = mapped_column(JSON, default=list)


class AutonomousTask(Base, TimestampMixin):
    __tablename__ = "autonomous_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("TASK"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    report_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    priority: Mapped[str] = mapped_column(String(32), default="default")
    status: Mapped[str] = mapped_column(String(32), default="open")


class Entity(Base, TimestampMixin):
    __tablename__ = "entities"
    __table_args__ = (UniqueConstraint("tenant_id", "normalized_name", "entity_type", name="uq_entity_tenant_name_type"), Index("ix_entities_tenant_type", "tenant_id", "entity_type"))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("ENT"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), index=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    source_report_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CollectionJob(Base, TimestampMixin):
    __tablename__ = "collection_jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(96), default=lambda: public_id("JOB"), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    target: Mapped[str] = mapped_column(String(255), index=True)
    target_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    raw_count: Mapped[int] = mapped_column(Integer, default=0)
    enriched_count: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[list[Any]] = mapped_column(JSON, default=list)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
