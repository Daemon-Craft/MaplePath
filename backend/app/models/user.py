import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.database import metadata

# Users table
users = sa.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(255), unique=True, index=True, nullable=False),
    Column("hashed_password", String(255), nullable=True),
    Column("full_name", String(255), nullable=True),
    Column("firebase_uid", String(255), unique=True, nullable=True, index=True),
    Column("is_active", Boolean, default=True),
    Column("is_verified", Boolean, default=False),
    Column("phone_number", String(20), nullable=True),
    Column("profile_picture_url", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Settle regions table
settle_regions = sa.Table(
    "settle_regions",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("region_name", String(255), unique=True, nullable=False, index=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Settle purposes table
settle_purposes = sa.Table(
    "settle_purposes",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("region_id", Integer, ForeignKey("settle_regions.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("purpose_name", String(255), nullable=False),
    Column("description", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# User settle purposes (junction table with progress tracking)
user_settle_purposes = sa.Table(
    "user_settle_purposes",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("settle_purpose_id", Integer, ForeignKey("settle_purposes.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("status", String(50), default="pending", nullable=False),  # pending, in_progress, completed
    Column("progression", Integer, default=0, nullable=False),  # 0-100
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)
