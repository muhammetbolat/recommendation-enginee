"""create content_score table

Revision ID: dfaefdd2c0d3
Revises: fdb139d0dca4
Create Date: 2021-08-01 02:32:00.875385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfaefdd2c0d3'
down_revision = 'fdb139d0dca4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('content_score',
                    sa.Column('productId', sa.String(length=1000), nullable=False),
                    sa.Column('score',  sa.String(length=4000), nullable=False),

                    sa.ForeignKeyConstraint(['productId'], ['ai_recommendation.meta.productId'], ),
                    schema='ai_recommendation'
                    )


def downgrade():
    op.drop_table('content_score', schema='ai_recommendation')
