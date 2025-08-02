import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from backend.db.tables import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "wildlife_db")


def build_url(db: str) -> str:
    """Build the database URL."""
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db}"


def get_engine(db: str, echo: bool = False, autocommit: bool = False) -> Engine:
    url = build_url(db)
    return create_engine(
        url, echo=echo, isolation_level="AUTOCOMMIT" if autocommit else None
    )


@contextmanager
def get_session() -> Iterator[Session]:
    """Provide a transactional scope around a series of ORM operations."""
    engine = get_engine(DB_NAME)
    local_session = sessionmaker(bind=engine)
    session = local_session()
    try:
        logger.info("→ Starting a new database session...")
        yield session
        session.commit()
    except Exception:
        logger.exception("⚠️ Error in DB session, rolling back.")
        session.rollback()
        raise
    finally:
        logger.info("✔ Closing the database session.")
        session.close()


def ensure_database_exists() -> None:
    """Connect to 'postgres', create DB_NAME if it doesn't already exist."""
    default_engine = get_engine("postgres", autocommit=True)
    with default_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db"), {"db": DB_NAME}
        ).scalar()
        if not exists:
            logger.info(f"→ Creating database '{DB_NAME}'...")
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            logger.info("✔ Database created.")
        else:
            logger.info(f"→ Database '{DB_NAME}' already exists.")


def init_db() -> None:
    """Ensure DB exists, then create all tables from your models."""
    ensure_database_exists()
    engine = get_engine(DB_NAME)
    Base.metadata.create_all(bind=engine)
    logger.info("✔ Tables created successfully.")


def drop_db() -> None:
    """Drop all tables in the target database."""
    engine = get_engine(DB_NAME)
    Base.metadata.drop_all(bind=engine)
    logger.info("🗑 All tables dropped.")
