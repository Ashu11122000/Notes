from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

from app.core.config import settings


# Encode password (VERY IMPORTANT)
password = quote_plus(settings.DB_PASSWORD)

# Database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:{password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Engine
engine = create_engine(DATABASE_URL)


# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()