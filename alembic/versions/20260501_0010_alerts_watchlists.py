"""alerts and watchlists

Revision ID: 20260501_0010
Revises: 20260501_0009
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0010'
down_revision = '20260501_0009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'watchlists',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('watchlist_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('terms', sa.JSON(), nullable=True),
        sa.Column('entity_ids', sa.JSON(), nullable=True),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_watchlists_watchlist_id', 'watchlists', ['watchlist_id'], unique=True)

    op.create_table(
        'alert_rules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('rule_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('scope', sa.String(length=64), nullable=False),
        sa.Column('rule_type', sa.String(length=64), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_alert_rules_rule_id', 'alert_rules', ['rule_id'], unique=True)

    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('alert_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=True),
        sa.Column('rule_id', sa.String(length=64), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('severity', sa.String(length=32), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=True),
        sa.Column('claim_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_alerts_alert_id', 'alerts', ['alert_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_alerts_alert_id', table_name='alerts')
    op.drop_table('alerts')
    op.drop_index('ix_alert_rules_rule_id', table_name='alert_rules')
    op.drop_table('alert_rules')
    op.drop_index('ix_watchlists_watchlist_id', table_name='watchlists')
    op.drop_table('watchlists')
