"""empty message

Revision ID: 3cad90b3b96a
Revises: 62e753977e3f
Create Date: 2020-11-05 14:24:17.951941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cad90b3b96a'
down_revision = '62e753977e3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('subscription_id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.drop_column('subscription_id')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
