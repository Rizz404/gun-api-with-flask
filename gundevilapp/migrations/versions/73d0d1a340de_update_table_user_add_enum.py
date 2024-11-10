"""update table user add enum

Revision ID: 73d0d1a340de
Revises: 00048804d6b2
Create Date: 2024-11-10 11:58:37.726845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73d0d1a340de'
down_revision = '00048804d6b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.TEXT(),
               type_=sa.Enum('USER', 'ADMIN', name='roleenum'),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.Enum('USER', 'ADMIN', name='roleenum'),
               type_=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###