"""init

Revision ID: 3267a9fbc101
Revises: 
Create Date: 2025-06-24 11:55:44.265530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3267a9fbc101'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('recipients',
    sa.Column('recipient_id', sa.BigInteger(), nullable=False),
    sa.Column('recipient_email', sa.String(), nullable=False),
    sa.Column('recipient_username', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('recipient_id', name=op.f('pk_recipients')),
    sa.UniqueConstraint('recipient_username', name=op.f('uq_recipients_recipient_username'))
    )
    op.create_index(op.f('ix_recipients_recipient_email'), 'recipients', ['recipient_email'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_recipients_recipient_email'), table_name='recipients')
    op.drop_table('recipients')
