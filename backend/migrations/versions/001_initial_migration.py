"""Add users, settle_regions, settle_purposes, and user_settle_purposes tables

Revision ID: 001
Revises:
Create Date: 2025-10-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('firebase_uid', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('profile_picture_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)

    # Create settle_regions table
    op.create_table(
        'settle_regions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('region_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_settle_regions_id'), 'settle_regions', ['id'], unique=False)
    op.create_index(op.f('ix_settle_regions_region_name'), 'settle_regions', ['region_name'], unique=True)

    # Create settle_purposes table
    op.create_table(
        'settle_purposes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=False),
        sa.Column('purpose_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['region_id'], ['settle_regions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_settle_purposes_id'), 'settle_purposes', ['id'], unique=False)
    op.create_index(op.f('ix_settle_purposes_region_id'), 'settle_purposes', ['region_id'], unique=False)

    # Create user_settle_purposes table
    op.create_table(
        'user_settle_purposes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('settle_purpose_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('progression', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['settle_purpose_id'], ['settle_purposes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_settle_purposes_id'), 'user_settle_purposes', ['id'], unique=False)
    op.create_index(op.f('ix_user_settle_purposes_user_id'), 'user_settle_purposes', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_settle_purposes_settle_purpose_id'), 'user_settle_purposes', ['settle_purpose_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_user_settle_purposes_settle_purpose_id'), table_name='user_settle_purposes')
    op.drop_index(op.f('ix_user_settle_purposes_user_id'), table_name='user_settle_purposes')
    op.drop_index(op.f('ix_user_settle_purposes_id'), table_name='user_settle_purposes')
    op.drop_table('user_settle_purposes')

    op.drop_index(op.f('ix_settle_purposes_region_id'), table_name='settle_purposes')
    op.drop_index(op.f('ix_settle_purposes_id'), table_name='settle_purposes')
    op.drop_table('settle_purposes')

    op.drop_index(op.f('ix_settle_regions_region_name'), table_name='settle_regions')
    op.drop_index(op.f('ix_settle_regions_id'), table_name='settle_regions')
    op.drop_table('settle_regions')

    op.drop_index(op.f('ix_users_firebase_uid'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
