"""empty message

Revision ID: 088bd2ef80af
Revises: e29d34e31d80
Create Date: 2016-11-29 17:12:48.626743

"""

# revision identifiers, used by Alembic.
revision = '088bd2ef80af'
down_revision = 'e29d34e31d80'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fmpath', table_name='xiangces')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('fmpath', 'xiangces', ['fmpath'], unique=True)
    ### end Alembic commands ###