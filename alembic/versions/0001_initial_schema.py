"""initial SOLACE schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-26
"""

from __future__ import annotations

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Generate concrete DDL with: make migration && make migrate
    # The ORM metadata is imported by alembic/env.py and is the canonical source.
    pass


def downgrade() -> None:
    pass
