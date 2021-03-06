"""empty message

Revision ID: 0d861b70da98
Revises: 7efbfe469a8a
Create Date: 2020-08-13 15:01:01.331351

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils.types.choice

# revision identifiers, used by Alembic.
revision = '0d861b70da98'
down_revision = '7efbfe469a8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('body', sa.String(length=1000), nullable=False),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(choices=[('D', 'DRAFT'), ('U', 'UNPUBLISHED'), ('P', 'PUBLISHED')]), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('modified_on', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
