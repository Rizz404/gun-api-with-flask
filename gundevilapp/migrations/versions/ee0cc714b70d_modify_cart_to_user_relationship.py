"""modify cart to user relationship

Revision ID: ee0cc714b70d
Revises: 82a224180ab5
Create Date: 2024-11-10 17:20:21.438163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee0cc714b70d'
down_revision = '82a224180ab5'
branch_labels = None
depends_on = None


def upgrade():
  # ### commands auto generated by Alembic - please adjust! ###
  with op.batch_alter_table('cart', schema=None) as batch_op:
    batch_op.create_unique_constraint('uq_cart_user_id', ['user_id'])

  # ### end Alembic commands ###


def downgrade():
  # ### commands auto generated by Alembic - please adjust! ###
  with op.batch_alter_table('cart', schema=None) as batch_op:
    batch_op.drop_constraint('uq_cart_user_id', type_='unique')

  # ### end Alembic commands ###