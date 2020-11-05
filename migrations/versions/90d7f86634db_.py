"""empty message

Revision ID: 90d7f86634db
Revises: a760f687ee5d
Create Date: 2020-11-05 14:20:24.137925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90d7f86634db'
down_revision = 'a760f687ee5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('subscription_id', sa.Integer(), nullable=False))
        batch_op.create_index(batch_op.f('ix_subscription_age'), ['age'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_subscription_age'))
        batch_op.drop_column('subscription_id')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
