"""empty message

Revision ID: 028873ae5124
Revises: 649930bd24ed
Create Date: 2016-11-24 15:30:19.385912

"""

# revision identifiers, used by Alembic.
revision = '028873ae5124'
down_revision = '649930bd24ed'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fmpath', table_name='tupians')
    op.drop_column('tupians', 'fmpath')
    op.add_column('xiangces', sa.Column('fmpath', sa.String(length=128), nullable=True))
    op.create_unique_constraint(None, 'xiangces', ['fmpath'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'xiangces', type_='unique')
    op.drop_column('xiangces', 'fmpath')
    op.add_column('tupians', sa.Column('fmpath', mysql.VARCHAR(length=128), nullable=True))
    op.create_index('fmpath', 'tupians', ['fmpath'], unique=True)
    ### end Alembic commands ###