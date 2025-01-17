"""Add User Roles Relationships

Revision ID: 4a822909a3ed
Revises: 5cd1b8648a3b
Create Date: 2024-07-04 10:09:48.723336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a822909a3ed'
down_revision = '5cd1b8648a3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_user_roles_role_id_role')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_roles_user_id_users'))
    )
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_constraint('fk_role_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index('ix_token_blocklist_jti')
        batch_op.create_index(batch_op.f('ix_token_blocklist_jti'), ['jti'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blocklist_jti'))
        batch_op.create_index('ix_token_blocklist_jti', ['jti'], unique=False)

    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_role_user_id_users', 'users', ['user_id'], ['id'])

    op.drop_table('user_roles')
    # ### end Alembic commands ###
