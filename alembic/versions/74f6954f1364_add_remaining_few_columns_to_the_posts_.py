"""add remaining few columns to the posts table

Revision ID: 74f6954f1364
Revises: bfe81f4ab2d9
Create Date: 2022-06-15 12:27:19.038298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74f6954f1364'
down_revision = 'bfe81f4ab2d9'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass