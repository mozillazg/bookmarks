"""empty message

Revision ID: dd702ee8401b
Revises: 8663dfffd2cc
Create Date: 2016-01-26 16:59:50.838718

"""

# revision identifiers, used by Alembic.
revision = 'dd702ee8401b'
down_revision = '8663dfffd2cc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'categories', ['name'])
    op.create_unique_constraint(None, 'tags', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='unique')
    op.drop_constraint(None, 'categories', type_='unique')
    ### end Alembic commands ###
