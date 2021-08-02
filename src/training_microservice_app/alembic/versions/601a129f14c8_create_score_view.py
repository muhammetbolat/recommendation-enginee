"""create score_view

Revision ID: 601a129f14c8
Revises: dfaefdd2c0d3
Create Date: 2021-08-01 02:59:35.021522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '601a129f14c8'
down_revision = 'dfaefdd2c0d3'
branch_labels = None
depends_on = None

upgrade_query = "create view \"ai_recommendation\".\"score_view\" as " \
                "select cart.\"productId\", cart.score as cart_score, passed.score as passed_score, content_s.score as " \
                "content_score from ai_recommendation.cart_score cart inner join ai_recommendation.passed_day_score passed " \
                "on cart.\"productId\" = passed.\"productId\" inner join ai_recommendation.content_score content_s on " \
                "passed.\"productId\" = content_s.\"productId\""


downgrade_query = "drop view \"ai_recommendation\".\"score_view\""


def upgrade():
    op.execute(upgrade_query)


def downgrade():
    op.execute(downgrade_query)

