"""create passed_day_score table

Revision ID: fdb139d0dca4
Revises: b3b86012827d
Create Date: 2021-07-30 09:24:16.541302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdb139d0dca4'
down_revision = 'b3b86012827d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('passed_day_score',
                    sa.Column('productId', sa.String(length=1000), nullable=False),
                    sa.Column('score', sa.Float(), nullable=False),

                    sa.ForeignKeyConstraint(['productId'], ['ai_recommendation.meta.productId'], ),
                    schema='ai_recommendation'
                    )


def downgrade():
    op.drop_table('passed_day_score', schema='ai_recommendation')
