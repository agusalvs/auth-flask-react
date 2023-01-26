"""empty message

Revision ID: 2414da015cd0
Revises: a0df81ff7e11
Create Date: 2023-01-26 14:30:25.880068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2414da015cd0'
down_revision = 'a0df81ff7e11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('birth_year', sa.String(length=250), nullable=False),
    sa.Column('homeworld', sa.String(length=250), nullable=False),
    sa.Column('starship', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###
