"""claims and evidence items

Revision ID: 20260501_0006
Revises: 20260501_0005
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0006'
down_revision = '20260501_0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'claims',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('claim_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('document_id', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('normalized_text', sa.Text(), nullable=False),
        sa.Column('claim_type', sa.String(length=64), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('verification_status', sa.String(length=32), nullable=False),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_claims_claim_id', 'claims', ['claim_id'], unique=True)

    op.create_table(
        'evidence_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('evidence_id', sa.String(length=64), nullable=False),
        sa.Column('claim_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('document_id', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('chunk_id', sa.String(length=64), nullable=False),
        sa.Column('start_offset', sa.Integer(), nullable=False),
        sa.Column('end_offset', sa.Integer(), nullable=False),
        sa.Column('excerpt_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_evidence_items_evidence_id', 'evidence_items', ['evidence_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_evidence_items_evidence_id', table_name='evidence_items')
    op.drop_table('evidence_items')
    op.drop_index('ix_claims_claim_id', table_name='claims')
    op.drop_table('claims')
