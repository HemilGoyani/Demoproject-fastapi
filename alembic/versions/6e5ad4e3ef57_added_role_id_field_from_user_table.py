"""added  role_id field from user table

Revision ID: 6e5ad4e3ef57
Revises: 
Create Date: 2022-01-26 02:25:27.141850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e5ad4e3ef57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_role_id', table_name='users')
    op.drop_column('users', 'role_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_users_role_id', 'users', ['role_id'], unique=False)
    # ### end Alembic commands ###
