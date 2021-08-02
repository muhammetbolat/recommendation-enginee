"""log

Revision ID: 157610c049be
Revises: 
Create Date: 2021-04-25 19:48:48.254014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157610c049be'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.execute('create schema "ai_recommendation"')
    op.create_table('log',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('level', sa.String(length=1000), nullable=False),
                    sa.Column('message', sa.String(length=4000), nullable=False),
                    sa.Column('logDatetime', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    schema='ai_recommendation'
                    )

    op.create_table('meta',
                    sa.Column('productId', sa.String(length=1000), nullable=False),
                    sa.Column('brand', sa.String(length=1000), nullable=False),
                    sa.Column('category', sa.String(length=1000), nullable=False),
                    sa.Column('subcategory', sa.String(length=1000), nullable=False),
                    sa.Column('name', sa.String(length=4000), nullable=False),

                    sa.PrimaryKeyConstraint('productId'),
                    schema='ai_recommendation'
                    )

    op.create_table('event',
                    sa.Column('productId', sa.String(length=1000), nullable=False),
                    sa.Column('numberOfCart', sa.Integer(), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('passedDay', sa.Integer(), nullable=False),

                    sa.ForeignKeyConstraint(['productId'], ['ai_recommendation.meta.productId'], ),
                    schema='ai_recommendation'
                    )

def downgrade():
    op.drop_table('log', schema='ai_recommendation')
    op.drop_table('event', schema='ai_recommendation')
    op.drop_table('meta', schema='ai_recommendation')
    op.execute('drop schema "ai_recommendation"')

