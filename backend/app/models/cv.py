import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from app.db.database import metadata

# Industries table (pre-loaded Canadian industries)
industries = sa.Table(
    "industries",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(255), unique=True, nullable=False, index=True),
    Column("name_fr", String(255), nullable=True),  # French translation
    Column("description", Text, nullable=True),
    Column("tips", JSON, nullable=True),  # Job-specific tips as JSON array
    Column("keywords", JSON, nullable=True),  # Industry keywords for CV optimization
    Column("is_active", Boolean, default=True, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# User CVs table
user_cvs = sa.Table(
    "user_cvs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("industry_id", Integer, ForeignKey("industries.id", ondelete="SET NULL"), nullable=True, index=True),
    Column("title", String(255), nullable=False),
    Column("full_name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("phone", String(50), nullable=True),
    Column("location", String(255), nullable=True),  # City, Province
    Column("summary", Text, nullable=True),
    Column("experience", JSON, nullable=True),  # Array of work experiences
    Column("education", JSON, nullable=True),  # Array of education entries
    Column("skills", JSON, nullable=True),  # Array of skills
    Column("certifications", JSON, nullable=True),  # Array of certifications
    Column("languages", JSON, nullable=True),  # Array of languages with proficiency
    Column("cv_content", JSON, nullable=False),  # Full generated CV content
    Column("format_type", String(50), default="canadian", nullable=False),  # canadian, chronological, functional
    Column("pdf_url", Text, nullable=True),  # S3 or Cloud Storage URL
    Column("is_favorite", Boolean, default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# CV Generation History (for tracking Vertex AI generations)
cv_generation_history = sa.Table(
    "cv_generation_history",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("cv_id", Integer, ForeignKey("user_cvs.id", ondelete="CASCADE"), nullable=True, index=True),
    Column("prompt", Text, nullable=False),  # AI prompt used
    Column("industry_id", Integer, ForeignKey("industries.id", ondelete="SET NULL"), nullable=True),
    Column("status", String(50), default="pending", nullable=False),  # pending, completed, failed
    Column("generated_content", JSON, nullable=True),
    Column("error_message", Text, nullable=True),
    Column("tokens_used", Integer, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)
