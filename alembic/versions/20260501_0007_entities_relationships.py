"""entities and relationships foundation

Revision ID: 20260501_0007
Revises: 20260501_0006
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0007'
down_revision = '20260501_0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('entities', sa.Column('case_id', sa.String(length=64), nullable=True, server_default=''))
    op.add_column('entities', sa.Column('entity_type', sa.String(length=64), nullable=True, server_default='unknown'))
    op.add_column('entities', sa.Column('canonical_name', sa.String(length=255), nullable=True))
    op.add_column('entities', sa.Column('aliases', sa.JSON(), nullable=True))
    op.add_column('entities', sa.Column('confidence_score', sa.Float(), nullable=True, server_default='0.5'))
    op.add_column('entities', sa.Column('metadata_json', sa.JSON(), nullable=True))

    op.create_table(
        'entity_relationships',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('relationship_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('subject_entity_id', sa.String(length=64), nullable=False),
        sa.Column('predicate', sa.String(length=128), nullable=False),
        sa.Column('object_entity_id', sa.String(length=64), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=False),
        sa.Column('claim_id', sa.String(length=64), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_entity_relationships_relationship_id', 'entity_relationships', ['relationship_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_entity_relationships_relationship_id', table_name='entity_relationships')
    op.drop_table('entity_relationships')
    op.drop_column('entities', 'metadata_json')
    op.drop_column('entities', 'confidence_score')
    op.drop_column('entities', 'aliases')
    op.drop_column('entities', 'canonical_name')
    op.drop_column('entities', 'entity_type')
    op.drop_column('entities', 'case_id')
