"""create join view

Revision ID: b3b86012827d
Revises: f171acb5f370
Create Date: 2021-07-30 00:21:56.587530

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import DDLElement
from sqlalchemy.ext import compiler


# revision identifiers, used by Alembic.
revision = 'b3b86012827d'
down_revision = 'f171acb5f370'
branch_labels = None
depends_on = None

upgrade_query = "create view \"ai_recommendation\".\"all_data\" as " \
                "select m.\"productId\", e.\"numberOfCart\", e.\"passedDay\", m.brand, m.category, m.subcategory, m.\"name\" from " \
                "ai_recommendation.meta m inner join ai_recommendation.\"event\" e on " \
                " m.\"productId\" = e.\"productId\""

downgrade_query = "drop view \"ai_recommendation\".\"all_data\""


def upgrade():
    op.execute(upgrade_query)


def downgrade():
    op.execute(downgrade_query)
