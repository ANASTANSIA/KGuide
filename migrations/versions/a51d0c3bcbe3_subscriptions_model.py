"""subscriptions Model

Revision ID: a51d0c3bcbe3
Revises: c89eef4400dc
Create Date: 2020-11-16 19:27:02.196531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a51d0c3bcbe3'
down_revision = 'c89eef4400dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notification_name'), ['name'], unique=False)

    op.create_table('subscriptions',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('program', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['program'], ['program.program_id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'program')
    )
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_subscriptions_age'), ['age'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_subscriptions_age'))

    op.drop_table('subscriptions')
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notification_name'))

    op.drop_table('notification')
    # ### end Alembic commands ###
