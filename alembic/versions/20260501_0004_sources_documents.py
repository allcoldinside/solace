"""sources and documents tables

Revision ID: 20260501_0004
Revises: 20260501_0003
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0004'
down_revision = '20260501_0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('source_type', sa.String(length=32), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('uri', sa.String(length=1024), nullable=True),
        sa.Column('collection_method', sa.String(length=64), nullable=False),
        sa.Column('authorization_basis', sa.String(length=255), nullable=True),
        sa.Column('collected_at', sa.DateTime(), nullable=False),
        sa.Column('collected_by', sa.String(length=64), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_sources_source_id', 'sources', ['source_id'], unique=True)

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('document_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('mime_type', sa.String(length=128), nullable=False),
        sa.Column('object_key', sa.String(length=255), nullable=False),
        sa.Column('sha256_hash', sa.String(length=64), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_documents_document_id', 'documents', ['document_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_documents_document_id', table_name='documents')
    op.drop_table('documents')
    op.drop_index('ix_sources_source_id', table_name='sources')
    op.drop_table('sources')
