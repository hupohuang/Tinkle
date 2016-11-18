"""empty message

Revision ID: 649930bd24ed
Revises: c9f6bc1971d2
Create Date: 2016-11-16 18:08:40.049009

"""

# revision identifiers, used by Alembic.
revision = '649930bd24ed'
down_revision = 'c9f6bc1971d2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fengmians')
    op.add_column('tupians', sa.Column('fmpath', sa.String(length=128), nullable=True))
    op.add_column('tupians', sa.Column('lspath', sa.String(length=128), nullable=True))
    op.create_unique_constraint(None, 'tupians', ['fmpath'])
    op.create_unique_constraint(None, 'tupians', ['lspath'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tupians', type_='unique')
    op.drop_constraint(None, 'tupians', type_='unique')
    op.drop_column('tupians', 'lspath')
    op.drop_column('tupians', 'fmpath')
    op.create_table('fengmians',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('fmpath', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('xiangce_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('tupian_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('lspath', mysql.VARCHAR(length=128), nullable=True),
    sa.ForeignKeyConstraint(['tupian_id'], ['tupians.id'], name='fengmians_ibfk_1'),
    sa.ForeignKeyConstraint(['xiangce_id'], ['xiangces.id'], name='fengmians_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    ### end Alembic commands ###