"""email notifications and user verify

Revision ID: b1a2c3d4e5f6
Revises: a4382fcd0415
Create Date: 2026-05-13
"""

import sqlalchemy as sa
from alembic import op

revision = 'b1a2c3d4e5f6'
down_revision = 'a4382fcd0415'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'is_verified', sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )
    op.create_table(
        'email_notifications',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column('recipient', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('template_name', sa.String(length=120), nullable=False),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error_message', sa.String(length=1000), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('email_notifications')
    op.drop_column('users', 'is_verified')
