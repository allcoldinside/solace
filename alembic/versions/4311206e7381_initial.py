"""initial

Revision ID: 4311206e7381
Revises:
Create Date: 2026-05-05 13:34:52.846450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4311206e7381'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_tenants_tenant_id', 'tenants', ['tenant_id'], unique=True)

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(32), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_users_user_id', 'users', ['user_id'], unique=True)
    op.create_index('ix_users_tenant_id', 'users', ['tenant_id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('report_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('subject_type', sa.String(64), nullable=False),
        sa.Column('classification', sa.String(32), nullable=False),
        sa.Column('confidence', sa.String(32), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('full_markdown', sa.Text(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_reports_report_id', 'reports', ['report_id'], unique=True)
    op.create_index('ix_reports_tenant_id', 'reports', ['tenant_id'])
    op.create_index('ix_reports_subject', 'reports', ['subject'])

    op.create_table(
        'panel_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('report_id', sa.String(64), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('transcript', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_panel_sessions_session_id', 'panel_sessions', ['session_id'], unique=True)
    op.create_index('ix_panel_sessions_tenant_id', 'panel_sessions', ['tenant_id'])
    op.create_index('ix_panel_sessions_report_id', 'panel_sessions', ['report_id'])

    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_cases_case_id', 'cases', ['case_id'], unique=True)
    op.create_index('ix_cases_tenant_id', 'cases', ['tenant_id'])
    op.create_index('ix_cases_title', 'cases', ['title'])

    op.create_table(
        'watches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('watch_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('target', sa.String(255), nullable=False),
        sa.Column('target_type', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_watches_watch_id', 'watches', ['watch_id'], unique=True)
    op.create_index('ix_watches_tenant_id', 'watches', ['tenant_id'])
    op.create_index('ix_watches_target', 'watches', ['target'])

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('action', sa.String(128), nullable=False),
        sa.Column('actor', sa.String(255), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_audit_logs_tenant_id', 'audit_logs', ['tenant_id'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])

    op.create_table(
        'revoked_tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('jti', sa.String(128), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_revoked_tokens_jti', 'revoked_tokens', ['jti'], unique=True)
    op.create_index('ix_revoked_tokens_tenant_id', 'revoked_tokens', ['tenant_id'])

    op.create_table(
        'memory_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('report_id', sa.String(64), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('meta', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_memory_entries_tenant_id', 'memory_entries', ['tenant_id'])
    op.create_index('ix_memory_entries_report_id', 'memory_entries', ['report_id'])

    op.create_table(
        'autonomous_tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('task_id', sa.String(64), nullable=False),
        sa.Column('report_id', sa.String(64), nullable=False),
        sa.Column('kind', sa.String(64), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_autonomous_tasks_tenant_id', 'autonomous_tasks', ['tenant_id'])
    op.create_index('ix_autonomous_tasks_task_id', 'autonomous_tasks', ['task_id'], unique=True)
    op.create_index('ix_autonomous_tasks_report_id', 'autonomous_tasks', ['report_id'])

    op.create_table(
        'entities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('entity_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('kind', sa.String(64), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_entities_entity_id', 'entities', ['entity_id'], unique=True)
    op.create_index('ix_entities_tenant_id', 'entities', ['tenant_id'])
    op.create_index('ix_entities_name', 'entities', ['name'])
    op.create_index('ix_entities_kind', 'entities', ['kind'])
    op.create_index('ix_entities_tenant_name', 'entities', ['tenant_id', 'name'])

    op.create_table(
        'collection_jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('job_id', sa.String(64), nullable=False),
        sa.Column('tenant_id', sa.String(64), nullable=False),
        sa.Column('target', sa.String(255), nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_collection_jobs_job_id', 'collection_jobs', ['job_id'], unique=True)
    op.create_index('ix_collection_jobs_tenant_id', 'collection_jobs', ['tenant_id'])
    op.create_index('ix_collection_jobs_target', 'collection_jobs', ['target'])


def downgrade() -> None:
    op.drop_table('collection_jobs')
    op.drop_table('entities')
    op.drop_table('autonomous_tasks')
    op.drop_table('memory_entries')
    op.drop_table('revoked_tokens')
    op.drop_table('audit_logs')
    op.drop_table('watches')
    op.drop_table('cases')
    op.drop_table('panel_sessions')
    op.drop_table('reports')
    op.drop_table('users')
    op.drop_table('tenants')
