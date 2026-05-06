"""tasks and approval workflow

Revision ID: 20260501_0012
Revises: 20260501_0011
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0012'
down_revision = '20260501_0011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('task_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('priority', sa.String(length=32), nullable=False),
        sa.Column('assigned_to', sa.String(length=64), nullable=True),
        sa.Column('due_at', sa.DateTime(), nullable=True),
        sa.Column('source_type', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=True),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_tasks_task_id', 'tasks', ['task_id'], unique=True)

    op.create_table(
        'approval_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('approval_request_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('requested_action', sa.String(length=128), nullable=False),
        sa.Column('target_type', sa.String(length=64), nullable=False),
        sa.Column('target_id', sa.String(length=64), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('requested_by', sa.String(length=64), nullable=False),
        sa.Column('approved_by', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_approval_requests_approval_request_id', 'approval_requests', ['approval_request_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_approval_requests_approval_request_id', table_name='approval_requests')
    op.drop_table('approval_requests')
    op.drop_index('ix_tasks_task_id', table_name='tasks')
    op.drop_table('tasks')
