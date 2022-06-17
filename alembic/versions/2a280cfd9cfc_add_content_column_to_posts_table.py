"""add content column to posts table

Revision ID: 2a280cfd9cfc
Revises: 856dfd48a58f
Create Date: 2022-06-15 11:15:55.892762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a280cfd9cfc'
down_revision = '856dfd48a58f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
