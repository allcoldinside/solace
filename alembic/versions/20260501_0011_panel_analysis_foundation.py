"""panel analysis foundation

Revision ID: 20260501_0011
Revises: 20260501_0010
Create Date: 2026-05-01
"""

from alembic import op
import sqlalchemy as sa

revision = '20260501_0011'
down_revision = '20260501_0010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'panel_runs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('panel_run_id', sa.String(length=64), nullable=False),
        sa.Column('tenant_id', sa.String(length=64), nullable=False),
        sa.Column('case_id', sa.String(length=64), nullable=False),
        sa.Column('report_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('consensus_summary', sa.Text(), nullable=True),
        sa.Column('created_by', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_panel_runs_panel_run_id', 'panel_runs', ['panel_run_id'], unique=True)

    op.create_table(
        'agent_responses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('agent_response_id', sa.String(length=64), nullable=False),
        sa.Column('panel_run_id', sa.String(length=64), nullable=False),
        sa.Column('agent_role', sa.String(length=64), nullable=False),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('concerns_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_agent_responses_agent_response_id', 'agent_responses', ['agent_response_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_agent_responses_agent_response_id', table_name='agent_responses')
    op.drop_table('agent_responses')
    op.drop_index('ix_panel_runs_panel_run_id', table_name='panel_runs')
    op.drop_table('panel_runs')
