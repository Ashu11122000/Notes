from urllib.parse import quote_plus

from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

from app.core.config import settings


# Encode special characters in password
password = quote_plus(settings.DB_PASSWORD)

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:{password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()