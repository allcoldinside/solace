"""timeline entries

Revision ID: 20260501_0008
Revises: 20260501_0007
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0008'
down_revision = '20260501_0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'timeline_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('timeline_entry_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('event_time', sa.DateTime(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('claim_id', sa.String(length=64), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_timeline_entries_timeline_entry_id', 'timeline_entries', ['timeline_entry_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_timeline_entries_timeline_entry_id', table_name='timeline_entries')
    op.drop_table('timeline_entries')
