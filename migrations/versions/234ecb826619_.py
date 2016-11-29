"""empty message

Revision ID: 234ecb826619
Revises: 028873ae5124
Create Date: 2016-11-24 15:45:58.215637

"""

# revision identifiers, used by Alembic.
revision = '234ecb826619'
down_revision = '028873ae5124'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tupians', sa.Column('fm', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'tupians', ['fm'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tupians', type_='unique')
    op.drop_column('tupians', 'fm')
    ### end Alembic commands ###
