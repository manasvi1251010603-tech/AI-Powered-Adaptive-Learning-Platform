from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def get_database_url() -> str | None:
    return get_settings().database_url


def create_database_engine() -> Engine | None:
    database_url = get_database_url()
    if database_url is None:
        return None

    return create_engine(
        database_url,
        pool_pre_ping=True,
        future=True,
    )


engine = create_database_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
) if engine is not None else None


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
