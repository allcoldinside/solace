"""case management fields

Revision ID: 20260501_0003
Revises: 20260501_0002
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0003'
down_revision = '20260501_0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('cases', sa.Column('priority', sa.String(length=16), nullable=True, server_default='medium'))
    op.add_column('cases', sa.Column('created_by', sa.String(length=64), nullable=True, server_default='system'))
    op.add_column('cases', sa.Column('assigned_to', sa.String(length=64), nullable=True, server_default=''))
    op.add_column('cases', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('cases', sa.Column('closed_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('cases', 'closed_at')
    op.drop_column('cases', 'updated_at')
    op.drop_column('cases', 'assigned_to')
    op.drop_column('cases', 'created_by')
    op.drop_column('cases', 'priority')
