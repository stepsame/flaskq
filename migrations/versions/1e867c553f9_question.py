"""question

Revision ID: 1e867c553f9
Revises: 1bb63a5ee9e
Create Date: 2015-12-15 16:58:30.926329

"""

# revision identifiers, used by Alembic.
revision = '1e867c553f9'
down_revision = '1bb63a5ee9e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=64), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_timestamp'), 'questions', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_questions_timestamp'), table_name='questions')
    op.drop_table('questions')
    ### end Alembic commands ###
