"""document processing pipeline fields and chunks

Revision ID: 20260501_0005
Revises: 20260501_0004
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0005'
down_revision = '20260501_0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('processing_status', sa.String(length=32), nullable=True, server_default='pending'))
    op.add_column('documents', sa.Column('processing_error', sa.Text(), nullable=True, server_default=''))
    op.add_column('documents', sa.Column('processed_at', sa.DateTime(), nullable=True))

    op.create_table(
        'document_chunks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('chunk_id', sa.String(length=64), nullable=False),
        sa.Column('document_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('start_offset', sa.Integer(), nullable=False),
        sa.Column('end_offset', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_document_chunks_chunk_id', 'document_chunks', ['chunk_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_document_chunks_chunk_id', table_name='document_chunks')
    op.drop_table('document_chunks')
    op.drop_column('documents', 'processed_at')
    op.drop_column('documents', 'processing_error')
    op.drop_column('documents', 'processing_status')
