"""empty message

Revision ID: 85a38dffe43e
Revises: 
Create Date: 2020-10-13 01:14:45.447840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85a38dffe43e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('slug', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.drop_table('my_temp_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_temp_table',
    sa.Column('tmp', sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.drop_table('tag')
    # ### end Alembic commands ###
