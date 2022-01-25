"""emove sequence in email token ,28 jan

Revision ID: 0466b36a9103
Revises: da9ef1a17d52
Create Date: 2022-01-25 04:18:28.941553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0466b36a9103'
down_revision = 'da9ef1a17d52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_email_token_id'), 'email_token', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_email_token_id'), table_name='email_token')
    # ### end Alembic commands ###