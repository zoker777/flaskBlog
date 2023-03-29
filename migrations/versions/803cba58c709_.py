"""empty message

Revision ID: 803cba58c709
Revises: 11ec2990ddc4
Create Date: 2022-09-01 10:42:38.130392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '803cba58c709'
down_revision = '11ec2990ddc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('photo_name', sa.String(length=50), nullable=False),
    sa.Column('photo_datetime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo')
    # ### end Alembic commands ###
