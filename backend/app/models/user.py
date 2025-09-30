import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.db.database import metadata

# Users table
users = sa.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(255), unique=True, index=True, nullable=False),
    Column("hashed_password", String(255), nullable=True),  # Nullable for Google auth users
    Column("full_name", String(255), nullable=True),
    Column("firebase_uid", String(255), unique=True, nullable=True, index=True),  # For Google auth
    Column("is_active", Boolean, default=True),
    Column("is_verified", Boolean, default=False),
    Column("phone_number", String(20), nullable=True),
    Column("profile_picture_url", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)
