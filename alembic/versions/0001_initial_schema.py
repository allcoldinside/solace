"""initial SOLACE schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("settings", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(64), nullable=False, server_default="analyst", index=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("report_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("subject", sa.String(255), nullable=False, index=True),
        sa.Column("subject_type", sa.String(64), nullable=False, index=True),
        sa.Column("classification", sa.String(32), nullable=False, server_default="TLP:WHITE"),
        sa.Column("confidence", sa.String(32), nullable=False, server_default="MEDIUM"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("executive_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("key_findings", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("entity_map", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("timeline", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("behavioral_indicators", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("threat_assessment", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("source_log", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("gaps", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("analyst_notes", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("full_markdown", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "panel_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("report_id", sa.String(96), nullable=False, index=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="complete"),
        sa.Column("transcript", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("synthesis", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "cases",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("case_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("title", sa.String(255), nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "watches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("watch_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("target", sa.String(255), nullable=False, index=True),
        sa.Column("target_type", sa.String(64), nullable=False, server_default="unknown"),
        sa.Column("cadence", sa.String(32), nullable=False, server_default="daily"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("audit_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("actor_user_id", sa.String(96), nullable=True, index=True),
        sa.Column("action", sa.String(128), nullable=False, index=True),
        sa.Column("resource_type", sa.String(64), nullable=False, index=True),
        sa.Column("resource_id", sa.String(96), nullable=True, index=True),
        sa.Column("details", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "revoked_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("jti", sa.String(128), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "memory_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("memory_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("report_id", sa.String(96), nullable=True, index=True),
        sa.Column("entity_id", sa.String(96), nullable=True, index=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "autonomous_tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("report_id", sa.String(96), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("priority", sa.String(32), nullable=False, server_default="default"),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "entities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("entity_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("normalized_name", sa.String(255), nullable=False, index=True),
        sa.Column("entity_type", sa.String(64), nullable=False, index=True),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("attributes", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("source_report_ids", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("tenant_id", "normalized_name", "entity_type", name="uq_entity_tenant_name_type"),
    )
    op.create_index("ix_entities_tenant_type", "entities", ["tenant_id", "entity_type"])

    op.create_table(
        "collection_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("job_id", sa.String(96), nullable=False, unique=True, index=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, server_default="default", index=True),
        sa.Column("target", sa.String(255), nullable=False, index=True),
        sa.Column("target_type", sa.String(64), nullable=False, index=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("raw_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enriched_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("errors", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("collection_jobs")
    op.drop_index("ix_entities_tenant_type", table_name="entities")
    op.drop_table("entities")
    op.drop_table("autonomous_tasks")
    op.drop_table("memory_entries")
    op.drop_table("revoked_tokens")
    op.drop_table("audit_logs")
    op.drop_table("watches")
    op.drop_table("cases")
    op.drop_table("panel_sessions")
    op.drop_table("reports")
    op.drop_table("users")
    op.drop_table("tenants")
