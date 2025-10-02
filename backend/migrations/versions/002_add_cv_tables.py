"""Add CV tables (industries, user_cvs, cv_generation_history)

Revision ID: 002
Revises: 001
Create Date: 2025-10-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create industries table
    op.create_table(
        'industries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('name_fr', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tips', JSON, nullable=True),
        sa.Column('keywords', JSON, nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_industries_id'), 'industries', ['id'], unique=False)
    op.create_index(op.f('ix_industries_name'), 'industries', ['name'], unique=True)

    # Create user_cvs table
    op.create_table(
        'user_cvs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('industry_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('experience', JSON, nullable=True),
        sa.Column('education', JSON, nullable=True),
        sa.Column('skills', JSON, nullable=True),
        sa.Column('certifications', JSON, nullable=True),
        sa.Column('languages', JSON, nullable=True),
        sa.Column('cv_content', JSON, nullable=False),
        sa.Column('format_type', sa.String(length=50), nullable=False, server_default='canadian'),
        sa.Column('pdf_url', sa.Text(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_cvs_id'), 'user_cvs', ['id'], unique=False)
    op.create_index(op.f('ix_user_cvs_user_id'), 'user_cvs', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_cvs_industry_id'), 'user_cvs', ['industry_id'], unique=False)

    # Create cv_generation_history table
    op.create_table(
        'cv_generation_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('cv_id', sa.Integer(), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('industry_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('generated_content', JSON, nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['cv_id'], ['user_cvs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cv_generation_history_id'), 'cv_generation_history', ['id'], unique=False)
    op.create_index(op.f('ix_cv_generation_history_user_id'), 'cv_generation_history', ['user_id'], unique=False)
    op.create_index(op.f('ix_cv_generation_history_cv_id'), 'cv_generation_history', ['cv_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_cv_generation_history_cv_id'), table_name='cv_generation_history')
    op.drop_index(op.f('ix_cv_generation_history_user_id'), table_name='cv_generation_history')
    op.drop_index(op.f('ix_cv_generation_history_id'), table_name='cv_generation_history')
    op.drop_table('cv_generation_history')

    op.drop_index(op.f('ix_user_cvs_industry_id'), table_name='user_cvs')
    op.drop_index(op.f('ix_user_cvs_user_id'), table_name='user_cvs')
    op.drop_index(op.f('ix_user_cvs_id'), table_name='user_cvs')
    op.drop_table('user_cvs')

    op.drop_index(op.f('ix_industries_name'), table_name='industries')
    op.drop_index(op.f('ix_industries_id'), table_name='industries')
    op.drop_table('industries')
