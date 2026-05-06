"""add user_tenant_memberships table

Revision ID: 20260501_0001
Revises: 
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_tenant_memberships',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('role', sa.String(length=32), nullable=False, server_default='analyst'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_user_tenant_memberships_user_tenant', 'user_tenant_memberships', ['user_id', 'tenant_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_user_tenant_memberships_user_tenant', table_name='user_tenant_memberships')
    op.drop_table('user_tenant_memberships')
