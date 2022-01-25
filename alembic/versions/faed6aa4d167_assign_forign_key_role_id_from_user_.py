"""assign forign key role_id from user_role table

Revision ID: faed6aa4d167
Revises: f83587933016
Create Date: 2022-01-25 16:01:40.510907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faed6aa4d167'
down_revision = 'f83587933016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_role', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index('ix_user_role_role_id', table_name='user_role')
    op.create_foreign_key(None, 'user_role', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_role', type_='foreignkey')
    op.create_index('ix_user_role_role_id', 'user_role', ['role_id'], unique=False)
    op.alter_column('user_role', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
