import databases
import sqlalchemy
from app.core.config import settings

# Database instance
database = databases.Database(settings.DATABASE_URL)

# SQLAlchemy metadata
metadata = sqlalchemy.MetaData()

# Database engine
engine = sqlalchemy.create_engine(settings.DATABASE_URL)
