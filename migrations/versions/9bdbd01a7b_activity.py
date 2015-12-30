"""activity

Revision ID: 9bdbd01a7b
Revises: 4f5df399a94
Create Date: 2015-12-28 11:25:22.480702

"""

# revision identifiers, used by Alembic.
revision = '9bdbd01a7b'
down_revision = '4f5df399a94'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('verb', sa.Unicode(length=255), nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), nullable=False),
    sa.Column('data', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('object_type', sa.String(length=255), nullable=True),
    sa.Column('object_id', sa.BigInteger(), nullable=True),
    sa.Column('object_tx_id', sa.BigInteger(), nullable=True),
    sa.Column('target_type', sa.String(length=255), nullable=True),
    sa.Column('target_id', sa.BigInteger(), nullable=True),
    sa.Column('target_tx_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_transaction_id'), 'activity', ['transaction_id'], unique=False)
    op.create_table('follows_version',
    sa.Column('follower_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('followed_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id', 'transaction_id')
    )
    op.create_index(op.f('ix_follows_version_end_transaction_id'), 'follows_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_follows_version_operation_type'), 'follows_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_follows_version_transaction_id'), 'follows_version', ['transaction_id'], unique=False)
    op.create_table('questions_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('body', sa.String(length=64), autoincrement=False, nullable=True),
    sa.Column('detail', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_questions_version_end_transaction_id'), 'questions_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_questions_version_operation_type'), 'questions_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_questions_version_timestamp'), 'questions_version', ['timestamp'], unique=False)
    op.create_index(op.f('ix_questions_version_transaction_id'), 'questions_version', ['transaction_id'], unique=False)
    op.create_table('votes_version',
    sa.Column('voter_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('answer_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('type', sa.Enum('up', 'down', name='vote_type'), autoincrement=False, nullable=True),
    sa.Column('timestamp', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('voter_id', 'answer_id', 'transaction_id')
    )
    op.create_index(op.f('ix_votes_version_end_transaction_id'), 'votes_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_votes_version_operation_type'), 'votes_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_votes_version_timestamp'), 'votes_version', ['timestamp'], unique=False)
    op.create_index(op.f('ix_votes_version_transaction_id'), 'votes_version', ['transaction_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_votes_version_transaction_id'), table_name='votes_version')
    op.drop_index(op.f('ix_votes_version_timestamp'), table_name='votes_version')
    op.drop_index(op.f('ix_votes_version_operation_type'), table_name='votes_version')
    op.drop_index(op.f('ix_votes_version_end_transaction_id'), table_name='votes_version')
    op.drop_table('votes_version')
    op.drop_index(op.f('ix_questions_version_transaction_id'), table_name='questions_version')
    op.drop_index(op.f('ix_questions_version_timestamp'), table_name='questions_version')
    op.drop_index(op.f('ix_questions_version_operation_type'), table_name='questions_version')
    op.drop_index(op.f('ix_questions_version_end_transaction_id'), table_name='questions_version')
    op.drop_table('questions_version')
    op.drop_index(op.f('ix_follows_version_transaction_id'), table_name='follows_version')
    op.drop_index(op.f('ix_follows_version_operation_type'), table_name='follows_version')
    op.drop_index(op.f('ix_follows_version_end_transaction_id'), table_name='follows_version')
    op.drop_table('follows_version')
    op.drop_index(op.f('ix_activity_transaction_id'), table_name='activity')
    op.drop_table('activity')
    ### end Alembic commands ###