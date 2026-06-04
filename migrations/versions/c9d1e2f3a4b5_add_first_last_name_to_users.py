"""add first_name and last_name to users

Revision ID: c9d1e2f3a4b5
Revises: b1a2c3d4e5f6
Create Date: 2026-06-04
"""

import sqlalchemy as sa
from alembic import op

revision = 'c9d1e2f3a4b5'
down_revision = 'b1a2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
