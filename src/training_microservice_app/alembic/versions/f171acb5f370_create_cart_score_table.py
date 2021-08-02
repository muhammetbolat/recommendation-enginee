"""create cart_score table

Revision ID: f171acb5f370
Revises: 157610c049be
Create Date: 2021-07-30 00:02:23.108702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f171acb5f370'
down_revision = '157610c049be'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cart_score',
                    sa.Column('productId', sa.String(length=1000), nullable=False),
                    sa.Column('score', sa.Float(), nullable=False),

                    sa.ForeignKeyConstraint(['productId'], ['ai_recommendation.meta.productId'], ),
                    schema='ai_recommendation'
                    )


def downgrade():
    op.drop_table('cart_score', schema='ai_recommendation')
