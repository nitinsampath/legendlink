"""Initial migration

Revision ID: f7cb35be3252
Revises: 
Create Date: 2025-01-25 05:50:52.086819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cb35be3252'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alembic auto-generates this code based on your model
    op.create_table('financial_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=True),
        sa.Column('date_uploaded', sa.DateTime(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('financial_records')
