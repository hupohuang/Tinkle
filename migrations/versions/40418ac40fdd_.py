"""empty message

Revision ID: 40418ac40fdd
Revises: f237c854c991
Create Date: 2016-12-15 15:13:50.146978

"""

# revision identifiers, used by Alembic.
revision = '40418ac40fdd'
down_revision = 'f237c854c991'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('xiangces', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'xiangces', 'users', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'xiangces', type_='foreignkey')
    op.drop_column('xiangces', 'user_id')
    ### end Alembic commands ###
