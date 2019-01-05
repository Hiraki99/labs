"""empty message

Revision ID: c376f841b4ce
Revises: 
Create Date: 2018-07-11 11:01:46.024897

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c376f841b4ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MasterKey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('key_private', sa.String(length=500), nullable=False),
    sa.Column('key_public', sa.String(length=500), nullable=False),
    sa.Column('wif', sa.String(length=500), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False),
    sa.Column('wallet_id_sqlite', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('createAt', sa.DateTime(), nullable=False),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.Column('root_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('key_private'),
    sa.UniqueConstraint('key_public'),
    sa.UniqueConstraint('path'),
    sa.UniqueConstraint('root_id'),
    sa.UniqueConstraint('wallet_id_sqlite'),
    sa.UniqueConstraint('wif')
    )
    op.create_index(op.f('ix_MasterKey_createAt'), 'MasterKey', ['createAt'], unique=False)
    op.create_index(op.f('ix_MasterKey_updateAt'), 'MasterKey', ['updateAt'], unique=False)
    op.create_table('RootKey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('main_network', sa.String(length=500), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=False),
    sa.Column('passphrase', sa.String(length=500), nullable=False),
    sa.Column('scheme', sa.String(length=100), nullable=False),
    sa.Column('createAt', sa.DateTime(), nullable=False),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('main_network'),
    sa.UniqueConstraint('passphrase'),
    sa.UniqueConstraint('scheme'),
    sa.UniqueConstraint('wallet_id')
    )
    op.create_index(op.f('ix_RootKey_createAt'), 'RootKey', ['createAt'], unique=False)
    op.create_index(op.f('ix_RootKey_updateAt'), 'RootKey', ['updateAt'], unique=False)
    op.create_table('SubKey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('key_private', sa.String(length=500), nullable=False),
    sa.Column('key_public', sa.String(length=500), nullable=False),
    sa.Column('wif', sa.String(length=500), nullable=False),
    sa.Column('path', sa.String(length=500), nullable=False),
    sa.Column('wallet_id_sqlite', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('key_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('useraccount_id', sa.Integer(), nullable=True),
    sa.Column('createAt', sa.DateTime(), nullable=False),
    sa.Column('updateAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('key_id'),
    sa.UniqueConstraint('key_private'),
    sa.UniqueConstraint('key_public'),
    sa.UniqueConstraint('path'),
    sa.UniqueConstraint('useraccount_id'),
    sa.UniqueConstraint('wallet_id_sqlite'),
    sa.UniqueConstraint('wif')
    )
    op.create_index(op.f('ix_SubKey_balance'), 'SubKey', ['balance'], unique=False)
    op.create_index(op.f('ix_SubKey_createAt'), 'SubKey', ['createAt'], unique=False)
    op.create_index(op.f('ix_SubKey_updateAt'), 'SubKey', ['updateAt'], unique=False)
    op.drop_table('Permission')
    op.drop_table('User')
    op.drop_index('ix_Transaction_createAt', table_name='Transaction')
    op.drop_index('ix_Transaction_currency', table_name='Transaction')
    op.drop_index('ix_Transaction_status', table_name='Transaction')
    op.drop_index('ix_Transaction_type', table_name='Transaction')
    op.drop_index('ix_Transaction_updateAt', table_name='Transaction')
    op.drop_index('ix_Transaction_value', table_name='Transaction')
    op.drop_table('Transaction')
    op.drop_index('ix_Account_balance', table_name='Account')
    op.drop_index('ix_Account_createAt', table_name='Account')
    op.drop_index('ix_Account_currency', table_name='Account')
    op.drop_index('ix_Account_subkey', table_name='Account')
    op.drop_index('ix_Account_type', table_name='Account')
    op.drop_table('Account')
    op.drop_table('Role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Role',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Role_id_seq"\'::regclass)'), nullable=False),
    sa.Column('name', sa.VARCHAR(length=125), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updateAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Role_pkey'),
    sa.UniqueConstraint('name', name='Role_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('Account',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Account_id_seq"\'::regclass)'), nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('account_no', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('subkey', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('balance', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('subkey_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lastest_transaction_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('live', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Account_pkey'),
    sa.UniqueConstraint('account_no', name='Account_account_no_key')
    )
    op.create_index('ix_Account_type', 'Account', ['type'], unique=False)
    op.create_index('ix_Account_subkey', 'Account', ['subkey'], unique=False)
    op.create_index('ix_Account_currency', 'Account', ['currency'], unique=False)
    op.create_index('ix_Account_createAt', 'Account', ['createAt'], unique=False)
    op.create_index('ix_Account_balance', 'Account', ['balance'], unique=False)
    op.create_table('Transaction',
    sa.Column('id', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('account_no', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('approver_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('kind', sa.VARCHAR(length=4), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('value', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('deposit_method', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('transaction_hash', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=False),
    sa.Column('live', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updateAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Transaction_pkey')
    )
    op.create_index('ix_Transaction_value', 'Transaction', ['value'], unique=False)
    op.create_index('ix_Transaction_updateAt', 'Transaction', ['updateAt'], unique=False)
    op.create_index('ix_Transaction_type', 'Transaction', ['type'], unique=False)
    op.create_index('ix_Transaction_status', 'Transaction', ['status'], unique=False)
    op.create_index('ix_Transaction_currency', 'Transaction', ['currency'], unique=False)
    op.create_index('ix_Transaction_createAt', 'Transaction', ['createAt'], unique=False)
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'), nullable=False),
    sa.Column('username', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('passwordresettoken', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('passwordresetexpires', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('confirmed_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('facebook', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('google', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('linkin', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('live', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updateAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=125), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='User_pkey'),
    sa.UniqueConstraint('email', name='User_email_key'),
    sa.UniqueConstraint('phone', name='User_phone_key'),
    sa.UniqueConstraint('username', name='User_username_key')
    )
    op.create_table('Permission',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Permission_id_seq"\'::regclass)'), nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('permission', sa.VARCHAR(length=125), autoincrement=False, nullable=False),
    sa.Column('permissionID', sa.VARCHAR(length=125), autoincrement=False, nullable=False),
    sa.Column('createAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updateAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], name='Permission_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Permission_pkey'),
    sa.UniqueConstraint('permissionID', name='Permission_permissionID_key')
    )
    op.drop_index(op.f('ix_SubKey_updateAt'), table_name='SubKey')
    op.drop_index(op.f('ix_SubKey_createAt'), table_name='SubKey')
    op.drop_index(op.f('ix_SubKey_balance'), table_name='SubKey')
    op.drop_table('SubKey')
    op.drop_index(op.f('ix_RootKey_updateAt'), table_name='RootKey')
    op.drop_index(op.f('ix_RootKey_createAt'), table_name='RootKey')
    op.drop_table('RootKey')
    op.drop_index(op.f('ix_MasterKey_updateAt'), table_name='MasterKey')
    op.drop_index(op.f('ix_MasterKey_createAt'), table_name='MasterKey')
    op.drop_table('MasterKey')
    # ### end Alembic commands ###