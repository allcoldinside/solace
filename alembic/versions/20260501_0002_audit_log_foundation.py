"""audit log foundation columns

Revision ID: 20260501_0002
Revises: 20260501_0001
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0002'
down_revision = '20260501_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('audit_logs', sa.Column('actor_user_id', sa.String(length=64), nullable=True))
    op.add_column('audit_logs', sa.Column('resource_type', sa.String(length=64), nullable=True))
    op.add_column('audit_logs', sa.Column('resource_id', sa.String(length=128), nullable=True))
    op.add_column('audit_logs', sa.Column('metadata_json', sa.JSON(), nullable=True))
    op.add_column('audit_logs', sa.Column('request_id', sa.String(length=128), nullable=True))
    op.add_column('audit_logs', sa.Column('ip_address', sa.String(length=64), nullable=True))
    op.add_column('audit_logs', sa.Column('user_agent', sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column('audit_logs', 'user_agent')
    op.drop_column('audit_logs', 'ip_address')
    op.drop_column('audit_logs', 'request_id')
    op.drop_column('audit_logs', 'metadata_json')
    op.drop_column('audit_logs', 'resource_id')
    op.drop_column('audit_logs', 'resource_type')
    op.drop_column('audit_logs', 'actor_user_id')
