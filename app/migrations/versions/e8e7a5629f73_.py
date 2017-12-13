"""empty message

Revision ID: e8e7a5629f73
Revises: a3edc48638b0
Create Date: 2017-12-13 09:47:35.248875

"""

# revision identifiers, used by Alembic.
revision = 'e8e7a5629f73'
down_revision = 'a3edc48638b0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    hotel = table('hotel', column('timezone'))
    op.execute(hotel.update().values(timezone='US/Eastern'))
    op.alter_column('hotel', 'timezone', nullable=False, existing_type=sa.String(length=50))


def downgrade():
    hotel = table('hotel', column('timezone'))
    op.alter_column('hotel', 'timezone', nullable=True, existing_type=sa.String(length=50))
