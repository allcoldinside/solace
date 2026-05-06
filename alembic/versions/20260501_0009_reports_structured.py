"""structured report fields

Revision ID: 20260501_0009
Revises: 20260501_0008
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0009'
down_revision = '20260501_0008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('reports', sa.Column('case_id', sa.String(length=64), nullable=True, server_default=''))
    op.add_column('reports', sa.Column('title', sa.String(length=255), nullable=True, server_default=''))
    op.add_column('reports', sa.Column('report_type', sa.String(length=64), nullable=True, server_default='case_summary'))
    op.add_column('reports', sa.Column('status', sa.String(length=32), nullable=True, server_default='draft'))
    op.add_column('reports', sa.Column('generated_by', sa.String(length=64), nullable=True, server_default='system'))
    op.add_column('reports', sa.Column('content_markdown', sa.Text(), nullable=True, server_default=''))
    op.add_column('reports', sa.Column('content_json', sa.JSON(), nullable=True))
    op.add_column('reports', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('reports', 'updated_at')
    op.drop_column('reports', 'content_json')
    op.drop_column('reports', 'content_markdown')
    op.drop_column('reports', 'generated_by')
    op.drop_column('reports', 'status')
    op.drop_column('reports', 'report_type')
    op.drop_column('reports', 'title')
    op.drop_column('reports', 'case_id')
